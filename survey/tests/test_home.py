from django.test import TestCase
from django.urls import reverse
from survey import models


class HomePageTest(TestCase):
    def test_reverse(self):
        self.assertEqual(reverse('home'), '/')

    def test_default_content(self):
        response = self.client.get(reverse('home'), follow=True)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'How X are you?')
        html = response.content.decode('utf8')
        # print(html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_uses_correct_template(self):
        response = self.client.get(reverse('home'), follow=True)
        self.assertTemplateUsed(response, 'survey/survey_list.html')
        models.Survey.objects.create(name='survey_1')
        response = self.client.get(reverse('home'), follow=True)
        self.assertTemplateUsed(response, 'survey/survey.html')
        models.Survey.objects.create(name='survey_2')
        response = self.client.get(reverse('home'), follow=True)
        self.assertTemplateUsed(response, 'survey/survey_list.html')
