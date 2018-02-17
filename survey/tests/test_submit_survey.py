from django.test import TestCase
from django.urls import reverse
from survey import models


class SubmitSurveyPageTest(TestCase):
    url_name = 'survey_submit'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name, args=['1']), '/survey/1/submit/')
