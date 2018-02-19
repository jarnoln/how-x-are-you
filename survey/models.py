from django.db import models
# from django.contrib import auth
from django.utils.translation import ugettext_lazy


class Survey(models.Model):
    """ Set of questions """
    name = models.SlugField(max_length=200, unique=True, verbose_name=ugettext_lazy('name'),
                            help_text=ugettext_lazy('Must be unique. Used in URL.'))
    title = models.CharField(max_length=250)
    description = models.TextField(default='', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE, related_name='blog_created_by')
    edited = models.DateTimeField(auto_now=True)

    @property
    def questions(self):
        return Question.objects.filter(survey=self).order_by('order', 'title')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['title']


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    title = models.CharField(max_length=250)
    description = models.TextField(default='', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}:{}:{}'.format(self.survey.name, self.order, self.title)


class Reference(models.Model):
    """ Set of reference answers to which user answers will be compared to """
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    name = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=250)
    description = models.TextField(default='', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def feedback(self, score):
        """ Find feedback corresponding to given score """
        feedbacks = Feedback.objects.filter(reference=self)
        exact = feedbacks.filter(exact_score=score)
        if exact.first():
            return exact.first()

        feedbacks = feedbacks.filter(exact_score=None)
        if score == 0:
            feedbacks = feedbacks.filter(min_score__lte=score)
        else:
            feedbacks = feedbacks.filter(min_score__lt=score)

        feedbacks = feedbacks.filter(max_score__gte=score)
        return feedbacks.first()

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE,
                                  null=True, blank=True, default=None)
    # user = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return '{}:{}'.format(self.question.title, self.value)


class Feedback(models.Model):
    """ Give a little feedback based on score """
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(default='', blank=True)
    exact_score = models.FloatField(null=True, blank=True, default=None)
    min_score = models.FloatField(default=0.0)
    max_score = models.FloatField(default=100.0)

    def __str__(self):
        if self.exact_score:
            return '{}:{} == {}'.format(self.reference.name, self.title, self.exact_score)
        else:
            return '{}:{}:from {} to {}'.format(self.reference.name, self.title, self.min_score, self.max_score)

    class Meta:
        ordering = ['min_score']
