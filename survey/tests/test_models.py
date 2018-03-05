# from unittest import skip
from django.test import TestCase
from django.contrib import auth
from survey.models import Survey, Question, Reference, Answer, Feedback


class SurveyModelTest(TestCase):
    def test_can_save_and_load(self):
        creator = auth.get_user_model().objects.create(username='creator')
        instance = Survey(creator=creator, name='philosophy', title='Philosophical questions')
        instance.save()
        self.assertEqual(Survey.objects.all().count(), 1)
        self.assertEqual(Survey.objects.all()[0], instance)

    def test_string(self):
        instance = Survey.objects.create(name='philosophy', title='Philosophical questions')
        self.assertEqual(str(instance), instance.name)

    def test_questions(self):
        survey = Survey.objects.create(name='philosophy', title='Philosophical questions')
        self.assertEqual(survey.questions.count(), 0)
        q1 = Question.objects.create(survey=survey, title='Why?')
        self.assertEqual(survey.questions.count(), 1)
        self.assertEqual(survey.questions.first(), q1)
        q2 = Question.objects.create(survey=survey, title='How?')
        self.assertEqual(survey.questions.count(), 2)
        self.assertEqual(survey.questions.first(), q2)
        q1.order = 1
        q2.order = 2
        q1.save()
        q2.save()
        self.assertEqual(survey.questions.first(), q1)


class QuestionModelTest(TestCase):
    def test_can_save_and_load(self):
        survey = Survey.objects.create(name='philosophy', title='Philosophical questions')
        instance = Question(survey=survey, title='Why?')
        instance.save()
        self.assertEqual(Question.objects.all().count(), 1)
        self.assertEqual(Question.objects.all()[0], instance)

    def test_string(self):
        survey = Survey.objects.create(name='philosophy', title='Philosophical questions')
        instance = Question.objects.create(survey=survey, title='Why?')
        self.assertEqual(str(instance), 'philosophy:0:Why?')


class ReferenceModelTest(TestCase):
    def test_can_save_and_load(self):
        survey = Survey.objects.create(name='philosophy', title='Philosophical questions')
        instance = Reference(survey=survey, name='plato', title='Plato')
        instance.save()
        self.assertEqual(Reference.objects.all().count(), 1)
        self.assertEqual(Reference.objects.all()[0], instance)

    def test_string(self):
        survey = Survey.objects.create(name='philosophy', title='Philosophical questions')
        instance = Reference.objects.create(survey=survey, name='plato', title='Plato')
        self.assertEqual(str(instance), instance.name)

    def test_feedback(self):
        survey = Survey.objects.create(name='philosophy', title='Philosophical questions')
        reference = Reference.objects.create(survey=survey, name='plato', title='Plato')
        self.assertEqual(reference.feedback(0), None)
        fb_1 = Feedback.objects.create(reference=reference, title='Grasshopper', min_score=0, max_score=25)
        fb_2 = Feedback.objects.create(reference=reference, title='On the fence', exact_score=50)
        fb_3 = Feedback.objects.create(reference=reference, title='Guru', min_score=75, max_score=100)
        self.assertEqual(reference.feedback(0), fb_1)
        self.assertEqual(reference.feedback(25), fb_1)
        self.assertEqual(reference.feedback(50), fb_2)
        self.assertEqual(reference.feedback(75), None)
        self.assertEqual(reference.feedback(80), fb_3)
        self.assertEqual(reference.feedback(100), fb_3)


class AnswerModelTest(TestCase):
    def test_can_save_and_load(self):
        survey = Survey.objects.create(name='philosophy', title='Philosophical questions')
        reference = Reference.objects.create(survey=survey, name='plato', title='Plato')
        question = Question.objects.create(survey=survey, title='Why?')
        instance = Answer(question=question, reference=reference, value=1)
        instance.save()
        self.assertEqual(Answer.objects.all().count(), 1)
        self.assertEqual(Answer.objects.all()[0], instance)

    def test_string(self):
        survey = Survey.objects.create(name='philosophy', title='Philosophical questions')
        reference = Reference.objects.create(survey=survey, name='plato', title='Plato')
        question = Question.objects.create(survey=survey, title='Why?')
        instance = Answer.objects.create(question=question, reference=reference, value=1)
        self.assertEqual(str(instance), 'Why?:1')


class FeedbackModelTest(TestCase):
    def test_can_save_and_load(self):
        survey = Survey.objects.create(name='philosophy', title='Philosophical questions')
        reference = Reference.objects.create(survey=survey, name='plato', title='Plato')
        instance = Feedback(reference=reference, title='Grasshopper', min_score=10, max_score=20)
        instance.save()
        self.assertEqual(Feedback.objects.all().count(), 1)
        self.assertEqual(Feedback.objects.all()[0], instance)

    def test_string(self):
        survey = Survey.objects.create(name='philosophy', title='Philosophical questions')
        reference = Reference.objects.create(survey=survey, name='plato', title='Plato')
        instance = Feedback.objects.create(reference=reference, title='Grasshopper', min_score=10, max_score=20)
        self.assertEqual(str(instance), 'plato:Grasshopper:from 10 to 20')
