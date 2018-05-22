from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator


class Question(models.Model):
    question = models.CharField(max_length=50)
    complexity = models.IntegerField(validators=[
            MaxValueValidator(20),
            MinValueValidator(5)
        ])


class Answer(models.Model):
    answer = models.CharField(max_length=30)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
