from django.urls import path

from . import views
from . import survey


urlpatterns = [
    path('survey/<int:survey_id>/submit/', views.submit_survey, name='survey_submit'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('', survey.SurveyView.as_view(), name='survey'),
]
