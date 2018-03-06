from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from survey import models
from users.tests.ext_test_case import ExtTestCase


class CreateQuestionPage(ExtTestCase):
    url_name = 'question_create'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name, args=['test_survey']), '/survey/test_survey/new/')

    def test_uses_correct_template(self):
        user = self.create_and_log_in_user()
        survey = models.Survey.objects.create(creator=user, name='test_survey')
        response = self.client.get(reverse(self.url_name, args=['test_survey']))
        self.assertTemplateUsed(response, 'survey/question_form.html')

    def test_default_context(self):
        user = self.create_and_log_in_user()
        survey = models.Survey.objects.create(creator=user, name='test_survey')
        response = self.client.get(reverse(self.url_name, args=[survey.name]))
        self.assertEqual(response.context['survey'], survey)
        # self.assertEqual(response.context['message'], '')

    def test_can_create_new_question(self):
        user = self.create_and_log_in_user()
        survey = models.Survey.objects.create(creator=user, name='test_survey')
        self.assertEqual(models.Question.objects.all().count(), 0)
        response = self.client.post(reverse(self.url_name, args=[survey.name]), {
            'title': 'Question 1',
            'description': 'For testing'},
                                    follow=True)
        self.assertEqual(models.Question.objects.all().count(), 1)
        self.assertEqual(models.Question.objects.first().survey, survey)
        self.assertEqual(models.Question.objects.first().title, 'Question 1')
        self.assertEqual(models.Question.objects.first().description, 'For testing')

    def test_cant_create_question_if_not_logged_in(self):
        creator = auth.get_user_model().objects.create(username='creator')
        survey = models.Survey.objects.create(creator=creator, name='test_survey')
        response = self.client.get(reverse(self.url_name, args=[survey.name]), follow=True)
        self.assertTemplateUsed(response, 'account/login.html')
