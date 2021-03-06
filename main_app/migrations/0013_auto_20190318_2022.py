# Generated by Django 2.1.7 on 2019-03-18 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_company_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='logo',
            new_name='address',
        ),
        migrations.AddField(
            model_name='company',
            name='phone',
            field=models.CharField(default=1111, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='role',
            field=models.CharField(choices=[('FoodGiver', 'FoodGiver'), ('FoodTaker', 'FoodTaker')], default='FoodTaker', max_length=12),
        ),
    ]
