from django.views.generic import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from survey.models import Survey, Question
from django.urls import reverse


class QuestionCreate(CreateView):
    model = Question
    fields = ['title', 'description']
    survey = None

    def dispatch(self, request, *args, **kwargs):
        survey_name = kwargs['survey_name']
        self.survey = get_object_or_404(Survey, name=survey_name)
        return super(QuestionCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.survey = self.survey
        return super(QuestionCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('survey_detail', args=[self.survey.name])

    def get_context_data(self, **kwargs):
        context = super(QuestionCreate, self).get_context_data(**kwargs)
        context['survey'] = self.survey
        # context['question'] = self.
        return context


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['title', 'description']
    survey = None

    def dispatch(self, request, *args, **kwargs):
        survey_name = kwargs['survey_name']
        self.survey = get_object_or_404(Survey, name=survey_name)
        return super(QuestionUpdate, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        # logger = logging.getLogger(__name__)
        # logger.warning('Tadaa!')
        if self.survey.can_edit(self.request.user):
            return super(QuestionUpdate, self).render_to_response(context, **response_kwargs)
        else:
            return HttpResponseRedirect(reverse('survey_detail', args=[self.survey.name]))

    def form_valid(self, form):
        if self.survey.can_edit(self.request.user):
            return super(QuestionUpdate, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse('survey_detail', args=[self.survey.name]))

    def get_success_url(self):
        return reverse('survey_detail', args=[self.survey.name])

    def get_context_data(self, **kwargs):
        context = super(QuestionUpdate, self).get_context_data(**kwargs)
        context['survey'] = self.survey
        return context
