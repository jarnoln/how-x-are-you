from django.urls import path

from . import views
from . import survey


urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('', survey.SurveyView.as_view(), name='survey'),
]
