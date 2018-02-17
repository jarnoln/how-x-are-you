from django.views.generic import TemplateView
from survey.models import Survey


class SurveyView(TemplateView):
    template_name = 'survey/survey.html'

    def get_context_data(self, **kwargs):
        survey = Survey.objects.first()
        context = super(SurveyView, self).get_context_data(**kwargs)
        context['survey'] = survey
        return context
