from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from survey import models
from users.tests.ext_test_case import ExtTestCase


class SurveyListTest(TestCase):
    url_name = 'survey_list'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name), '/surveys/')

    def test_uses_correct_template(self):
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'survey/survey_list.html')

    def test_default_context(self):
        creator = auth.get_user_model().objects.create(username='creator')
        survey_1 = models.Survey.objects.create(creator=creator, name="survey_1", title="Survey 1")
        survey_2 = models.Survey.objects.create(creator=creator, name="survey_2", title="Survey 2")
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

    def test_two_surveys(self):
        survey_1 = models.Survey.objects.create(name="survey_1", title="Survey 1")
        survey_2 = models.Survey.objects.create(name="survey_2", title="Survey 2")
        response = self.client.get(reverse(self.url_name, args=[survey_1.name]))
        self.assertEqual(response.context['survey'], survey_1)
        response = self.client.get(reverse(self.url_name, args=[survey_2.name]))
        self.assertEqual(response.context['survey'], survey_2)


class SurveyFirstPageTest(TestCase):
    url_name = 'survey_first'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name), '/survey/first/')

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


class CreateSurveyPage(ExtTestCase):
    url_name = 'survey_create'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name), '/create/')

    def test_uses_correct_template(self):
        self.create_and_log_in_user()
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, 'survey/survey_form.html')

    def test_default_context(self):
        self.create_and_log_in_user()
        # self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: 'en-us'})
        response = self.client.get(reverse(self.url_name))
        # self.assertEqual(response.context['title'], 'Create new blog')
        # self.assertEqual(response.context['message'], '')

    def test_can_create_new_survey(self):
        self.assertEqual(models.Survey.objects.all().count(), 0)
        user = self.create_and_log_in_user()
        response = self.client.post(reverse(self.url_name), {
            'name': 'test_survey',
            'title': 'Test survey',
            'description': 'For testing'},
                                    follow=True)
        self.assertEqual(models.Survey.objects.all().count(), 1)
        self.assertEqual(response.context['survey'].name, 'test_survey')
        self.assertEqual(response.context['survey'].title, 'Test survey')
        self.assertEqual(response.context['survey'].description, 'For testing')
        self.assertEqual(response.context['survey'].creator, user)

    def test_cant_create_survey_if_not_logged_in(self):
        response = self.client.get(reverse(self.url_name), follow=True)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_cant_create_survey_with_existing_name(self):
        user = self.create_and_log_in_user()
        models.Survey.objects.create(name="test_survey", title="Test survey")
        self.assertEqual(models.Survey.objects.all().count(), 1)
        # self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: 'en-us'})
        response = self.client.post(
            reverse(self.url_name),
            {
                'name': 'test_survey',
                'title': 'Test survey',
                'description': 'For testing'
            },
            follow=True)
        self.assertEqual(models.Survey.objects.all().count(), 1)
        self.assertTemplateUsed(response, 'survey/survey_form.html')
        # self.assertContains(response, 'Survey with this Name already exists')


class UpdateSurveyPage(ExtTestCase):
    url_name = 'survey_update'

    def test_reverse(self):
        self.assertEqual(reverse(self.url_name, args=['test_survey']), '/survey/test_survey/edit/')

    def test_uses_correct_template(self):
        user = self.create_and_log_in_user()
        survey = models.Survey.objects.create(creator=user, name="test_survey")
        response = self.client.get(reverse(self.url_name, args=[survey.name]))
        self.assertTemplateUsed(response, 'survey/survey_form.html')

    def test_404_no_survey(self):
        self.create_and_log_in_user()
        response = self.client.get(reverse(self.url_name, args=['test_blog']))
        self.assertTemplateUsed(response, '404.html')

    def test_can_update_survey(self):
        user = self.create_and_log_in_user()
        models.Survey.objects.create(creator=user, name="test_survey", title="Test survey", description="Testing")
        self.assertEqual(models.Survey.objects.all().count(), 1)
        response = self.client.post(reverse(self.url_name, args=['test_survey']), {
            'title': 'Test survey updated',
            'description': 'Updated'},
                                    follow=True)
        self.assertEqual(models.Survey.objects.all().count(), 1)
        survey = models.Survey.objects.all()[0]
        self.assertEqual(survey.title, 'Test survey updated')
        self.assertEqual(survey.description, 'Updated')
        self.assertTemplateUsed(response, 'survey/survey.html')
        self.assertEqual(response.context['survey'].title, 'Test survey updated')
        self.assertEqual(response.context['survey'].description, 'Updated')

    def test_cant_update_survey_if_not_logged_in(self):
        creator = auth.get_user_model().objects.create(username='creator')
        models.Survey.objects.create(creator=creator, name="test_survey", title="Test survey", description="Testing")
        response = self.client.post(reverse(self.url_name, args=['test_survey']), {
                                    'title': 'Test survey updated',
                                    'description': 'Updated'},
                                    follow=True)
        blog = models.Survey.objects.all()[0]
        self.assertEqual(blog.title, 'Test survey')
        self.assertEqual(blog.description, 'Testing')
        self.assertTemplateUsed(response, 'account/login.html')

    def test_cant_update_survey_if_not_creator(self):
        creator = auth.get_user_model().objects.create(username='creator')
        models.Survey.objects.create(creator=creator, name="test_survey", title="Test survey", description="Testing")
        self.create_and_log_in_user()
        response = self.client.post(reverse(self.url_name, args=['test_survey']), {
                                    'title': 'Test survey updated',
                                    'description': 'Updated'},
                                    follow=True)
        blog = models.Survey.objects.all()[0]
        self.assertEqual(blog.title, 'Test survey')
        self.assertEqual(blog.description, 'Testing')
        self.assertTemplateUsed(response, 'survey/survey.html')
