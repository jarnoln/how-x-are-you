from django.urls import path

from . import views
from . import survey
from .submit_survey import submit_survey

urlpatterns = [
    path('survey/first/', survey.SurveyView.as_view(), name='survey_first'),  # Show the first (usually the only) survey
    path('survey/<slug:survey_name>/submit/', submit_survey, name='survey_submit'),
    path('survey/<slug:survey_name>/', survey.SurveyView.as_view(), name='survey_detail'),
    path('surveys/', survey.SurveyList.as_view(), name='survey_list'),
    path('home/', views.HomeView.as_view(), name='home'),
]
