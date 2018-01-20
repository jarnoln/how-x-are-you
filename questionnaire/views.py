from django.views.generic import TemplateView
# from .upload import UploadForm


class HomeView(TemplateView):
    template_name = 'questionnaire/home.html'

