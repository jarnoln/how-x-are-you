from django.test import TestCase
from django.urls import reverse
from survey import models


class SurveyPageTest(TestCase):
    url_name = 'survey'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name), '/')

    def test_default_content(self):
        survey = models.Survey.objects.create(name="test_survey", title="Test survey")

        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['survey'], survey)
        self.assertContains(response, survey.title)
        html = response.content.decode('utf8')
        # print(html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_uses_correct_template(self):
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'survey/survey.html')
