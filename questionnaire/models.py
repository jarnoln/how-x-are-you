from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(default='', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
