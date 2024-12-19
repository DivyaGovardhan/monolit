import re
from dataclasses import fields

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.shortcuts import get_object_or_404

from .models import User, Question, Choice


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    email = forms.CharField(required=True, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    avatar = forms.FileField(required=True, label='Аватар', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])])
    password = forms.CharField(required=True, max_length=200, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password_confirm = forms.CharField(required=True, max_length=200, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Подтверждение пароля'}))
    consent = forms.BooleanField(required=True, label='Согласие на обработку персональных данных', widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Данное имя пользователя уже занято.')
        if not re.match(r'^[A-z-]+$', username):
            raise ValidationError('Имя пользователя должно содержать только латиницу и дефисы.')
        return username

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar.size > 1024 * 1024 * 2:
            raise ValidationError('Файл слишком большой. Размер не должен превышать 2 МБ.')
        return avatar

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError('Пароли должны совпадать.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=200, label='', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    password = forms.CharField(required=True, max_length=200, label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 1024 * 1024 * 2:
                raise ValidationError('Файл слишком большой. Размер не должен превышать 2 МБ.')
        return avatar

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.email = self.cleaned_data.get('email')
            user.avatar = self.cleaned_data.get('avatar')
            user.save()
        return user

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['short_desc', 'question_text', 'image']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']