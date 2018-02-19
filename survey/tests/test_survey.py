from django.test import TestCase
from django.urls import reverse
from survey import models


class SurveyListTest(TestCase):
    url_name = 'survey_list'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name), '/surveys/')

    def test_uses_correct_template(self):
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'survey/survey_list.html')

    def test_default_context(self):
        # creator = auth.get_user_model().objects.create(username='creator')
        survey_1 = models.Survey.objects.create(name="survey_1", title="Survey 1")
        survey_2 = models.Survey.objects.create(name="survey_2", title="Survey 2")
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.context['survey_list'].count(), 2)
        self.assertEqual(response.context['survey_list'][0], survey_1)
        self.assertEqual(response.context['survey_list'][1], survey_2)


class SurveyDetailPageTest(TestCase):
    url_name = 'survey_detail'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name, args=['test_survey']), '/survey/test_survey/')

    def test_default_content(self):
        survey = models.Survey.objects.create(name="test_survey", title="Test survey")
        q1 = models.Question.objects.create(survey=survey, title="Question 1")
        q2 = models.Question.objects.create(survey=survey, title="Question 2")
        response = self.client.get(reverse(self.url_name, args=[survey.name]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['survey'], survey)
        self.assertContains(response, survey.title)
        self.assertContains(response, q1.title)
        self.assertContains(response, q2.title)
        html = response.content.decode('utf8')
        # print(html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_uses_correct_template(self):
        survey = models.Survey.objects.create(name="test_survey", title="Test survey")
        response = self.client.get(reverse(self.url_name, args=[survey.name]))
        self.assertTemplateUsed(response, 'survey/survey.html')


class SurveyFirstPageTest(TestCase):
    url_name = 'survey_first'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name), '/')

    def test_default_content(self):
        survey = models.Survey.objects.create(name="test_survey", title="Test survey")
        q1 = models.Question.objects.create(survey=survey, title="Question 1")
        q2 = models.Question.objects.create(survey=survey, title="Question 2")
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['survey'], survey)
        self.assertContains(response, survey.title)
        self.assertContains(response, q1.title)
        self.assertContains(response, q2.title)
        html = response.content.decode('utf8')
        # print(html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_uses_correct_template(self):
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'survey/survey.html')
