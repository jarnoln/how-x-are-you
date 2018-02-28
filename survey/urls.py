from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from . import survey
from .submit_survey import submit_survey

urlpatterns = [
    path('survey/first/', survey.SurveyView.as_view(), name='survey_first'),  # Show the first (usually the only) survey
    path('survey/<slug:slug>/edit/', login_required(survey.SurveyUpdate.as_view()), name='survey_update'),
    path('survey/<slug:survey_name>/submit/', submit_survey, name='survey_submit'),
    path('survey/<slug:survey_name>/', survey.SurveyView.as_view(), name='survey_detail'),
    path('surveys/', survey.SurveyList.as_view(), name='survey_list'),
    path('create/', login_required(survey.SurveyCreate.as_view()), name='survey_create'),
    path('', views.home, name='home'),
]
