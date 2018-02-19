from django.urls import path

from . import views
from . import survey


urlpatterns = [
    path('survey/<slug:survey_name>/submit/', views.submit_survey, name='survey_submit'),
    path('surveys/', survey.SurveyList.as_view(), name='survey_list'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('', survey.SurveyView.as_view(), name='survey'),
]
