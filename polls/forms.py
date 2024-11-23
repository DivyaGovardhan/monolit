from django import forms
from django.core.exceptions import ValidationError
import re

from django.core.validators import FileExtensionValidator

from polls.models import User


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Имя пользователя', widget=forms.TextInput())
    email = forms.CharField(required=True, label='Электронная почта', widget=forms.TextInput())
    avatar = forms.FileField(required=True, label='Фото помещения', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])])
    password = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput())
    password_repeat = forms.CharField(required=True, label='Пароль повторно', widget=forms.PasswordInput())


    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Данное имя пользователя уже занято')
        if not re.match(r'^[A-z-]+$', username):
            raise ValidationError('Имя пользователя может содержать только латиницу и дефисы')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[A-z][\w.-]+@[\w.-]+\.[A-z]{2,6}$', email):
            raise ValidationError('Адрес электронной почты не валиден')
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar.size > 1024*1024*2:
            raise ValidationError('Файл слишком большой. Размер не должен превышать 2 МБ')
        return avatar

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        if password != password_repeat:
            raise ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user