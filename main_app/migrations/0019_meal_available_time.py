# Generated by Django 2.1.7 on 2019-03-20 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0018_remove_meal_available_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='available_time',
            field=models.TimeField(default='12:00PM', verbose_name='pickup'),
            preserve_default=False,
        ),
    ]
