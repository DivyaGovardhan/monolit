# Generated by Django 3.2.25 on 2024-11-23 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.FileField(upload_to='', verbose_name='Аватар'),
        ),
    ]
