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


class UpdateQuestionPage(ExtTestCase):
    url_name = 'question_update'

    def test_reverse_article_edit(self):
        self.assertEqual(reverse(self.url_name, args=['test_survey', 1]),
                         '/survey/test_survey/1/update/')

    def test_uses_correct_template(self):
        user = self.create_and_log_in_user()
        survey = models.Survey.objects.create(creator=user, name='test_survey')
        question = models.Question.objects.create(survey=survey, title="Question 1")
        response = self.client.get(reverse(self.url_name, args=[survey.name, question.id]))
        self.assertTemplateUsed(response, 'survey/question_form.html')

    def test_default_context(self):
        user = self.create_and_log_in_user()
        survey = models.Survey.objects.create(creator=user, name='test_survey')
        question = models.Question.objects.create(survey=survey, title="Question 1")
        response = self.client.get(reverse(self.url_name, args=[survey.name, question.id]))
        self.assertEqual(response.context['survey'], survey)
        self.assertEqual(response.context['question'], question)
        self.assertEqual(response.context['question'].survey, survey)
        # self.assertEqual(response.context['message'], '')

    def test_can_update_question(self):
        user = self.create_and_log_in_user()
        survey = models.Survey.objects.create(creator=user, name='test_survey')
        question = models.Question.objects.create(survey=survey, title="Question 1")
        self.assertEqual(models.Question.objects.all().count(), 1)
        response = self.client.post(reverse(self.url_name, args=[survey.name, question.id]),
                                    {'title': 'Question updated', 'description': 'Updated'},
                                    follow=True)
        self.assertEqual(models.Question.objects.all().count(), 1)
        question = models.Question.objects.all()[0]
        self.assertEqual(question.title, 'Question updated')
        self.assertEqual(question.description, 'Updated')
        self.assertTemplateUsed(response, 'survey/survey.html')
        self.assertEqual(response.context['survey'], survey)

    def test_cant_edit_without_logging_in(self):
        creator = auth.get_user_model().objects.create(username='creator')
        survey = models.Survey.objects.create(creator=creator, name='test_survey')
        question = models.Question.objects.create(survey=survey, title="Question 1")
        response = self.client.get(reverse(self.url_name, args=[survey.name, question.id]), follow=True)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_cant_edit_question_if_not_creator(self):
        creator = auth.get_user_model().objects.create(username='creator')
        survey = models.Survey.objects.create(creator=creator, name='test_survey')
        question = models.Question.objects.create(survey=survey, title="Question 1")
        self.create_and_log_in_user()
        response = self.client.post(reverse(self.url_name, args=[survey.name, question.id]),
                                    {'title': 'Question updated', 'description': 'Updated'},
                                    follow=True)
        self.assertTemplateUsed(response, 'survey/survey.html')
        self.assertEqual(models.Question.objects.all().count(), 1)
        question = models.Question.objects.all()[0]
        self.assertEqual(question.title, 'Question 1')
        self.assertEqual(question.description, '')
