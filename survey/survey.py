from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from survey.models import Survey
from django.urls import reverse


class SurveyList(ListView):
    model = Survey


class SurveyView(TemplateView):
    template_name = 'survey/survey.html'

    def get_context_data(self, **kwargs):
        survey_name = self.kwargs.get('survey_name')
        if survey_name:
            survey = get_object_or_404(Survey, name=survey_name)
        else:
            survey = Survey.objects.first()

        context = super(SurveyView, self).get_context_data(**kwargs)
        context['survey'] = survey
        return context


class SurveyCreate(CreateView):
    model = Survey
    slug_field = 'name'
    fields = ['name', 'title', 'description']

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(SurveyCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('survey_detail', args=[self.object.name])


class SurveyUpdate(UpdateView):
    model = Survey
    slug_field = 'name'
    fields = ['title', 'description']

    def render_to_response(self, context, **response_kwargs):
        # logger = logging.getLogger(__name__)
        # logger.warning('Tadaa!')
        # if self.object.can_edit(self.request.user):
        return super(SurveyUpdate, self).render_to_response(context, **response_kwargs)
        # else:
        #    return HttpResponseRedirect(reverse('survey_detail', args=[self.object.name]))

    def form_valid(self, form):
        # if self.object.can_edit(self.request.user):
        return super(SurveyUpdate, self).form_valid(form)
        # else:
        #    return HttpResponseRedirect(reverse('survey_detail', args=[self.object.name]))

    def get_success_url(self):
        return reverse('survey_detail', args=[self.object.name])
