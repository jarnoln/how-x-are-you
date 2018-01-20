# from unittest import skip
from django.test import TestCase
from questionnaire.models import Question


class QuestionModelTest(TestCase):
    def test_can_save_and_load(self):
        question = Question(title='Why?')
        question.save()
        self.assertEqual(Question.objects.all().count(), 1)
        self.assertEqual(Question.objects.all()[0], question)

    def test_string(self):
        question = Question.objects.create(title='Why?')
        self.assertEqual(str(question), question.title)
