import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import EmailField
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, verbose_name="Имя пользователя")
    email = EmailField(max_length=320, unique=True, verbose_name="Электронная почта")
    avatar = models.FileField(verbose_name="Аватар")
    password = models.CharField(max_length=100, verbose_name=True)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
