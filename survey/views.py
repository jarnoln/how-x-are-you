# from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Survey


def home(request):
    # surveys = Survey.objects.all()
    if Survey.objects.count() == 1:
        return HttpResponseRedirect(reverse('survey_detail', args=[Survey.objects.first().name]))
    else:
        return HttpResponseRedirect(reverse('survey_list'))
