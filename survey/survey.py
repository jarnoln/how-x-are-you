from django.views.generic import ListView, TemplateView
from django.shortcuts import get_object_or_404
from survey.models import Survey


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
