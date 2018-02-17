from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse


class HomeView(TemplateView):
    template_name = 'survey/home.html'


def submit_survey(request, survey_id):
    return HttpResponseRedirect(reverse('survey'))
