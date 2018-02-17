from django.test import TestCase
from django.urls import reverse
from survey import models


class SubmitSurveyPageTest(TestCase):
    url_name = 'survey_submit'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name, args=['ts']), '/survey/ts/submit/')

    def test_uses_correct_template(self):
        survey = models.Survey.objects.create(name="test_survey", title="Test survey")
        response = self.client.post(reverse(self.url_name, args=[survey.name]), follow=True)
        self.assertTemplateUsed(response, 'survey/result.html')

    def test_submit_survey(self):
        survey = models.Survey.objects.create(name="test_survey", title="Test survey")
        q1 = models.Question.objects.create(survey=survey, title="Question 1")
        response = self.client.post(reverse(self.url_name, args=[survey.name]),
                                    data={'q-{}'.format(q1.id): '10'},
                                    follow=True)
        self.assertEqual(response.context['survey'], survey)
        self.assertEqual(response.context['max_score'], 10)
        self.assertEqual(response.context['score'], 10)
        self.assertEqual(response.context['nscore'], 10)
        self.assertEqual(response.context['pct'], 100.0)
        self.assertEqual(response.context['npct'], 100.0)
        self.assertEqual(len(response.context['answers']), 1)
