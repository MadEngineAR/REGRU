# Generated by Django 3.2.6 on 2022-05-04 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='langs',
            field=models.CharField(blank=True, default='RU', max_length=10, verbose_name='Пол'),
        ),
    ]
