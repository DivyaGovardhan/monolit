import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=200, verbose_name='Имя пользователя', unique=True)
    email = models.EmailField(max_length=200, verbose_name='Email', unique=True)
    password = models.CharField(max_length=200, verbose_name='Пароль')
    avatar = models.FileField(verbose_name='Аватар', blank=False)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Question(models.Model):
    short_desc = models.CharField(max_length=200, verbose_name='Краткое описание')
    question_text = models.CharField(max_length=1000, verbose_name='Текст вопроса')
    image = models.FileField(verbose_name='Картинка', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    total_votes = models.IntegerField(default=0)
    voters = models.ManyToManyField('User', blank=True, related_name='voted_questions')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=3)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, verbose_name='Текст ответа')
    votes = models.IntegerField(default=0)

    def get_percent(self):
        return round(self.votes * 100 / self.question.total_votes) if self.votes != 0 else 0

    def __str__(self):
        return self.choice_text