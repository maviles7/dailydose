# Generated by Django 5.1.1 on 2024-10-11 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_remove_dose_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dose',
            name='url',
            field=models.URLField(max_length=1000),
        ),
    ]
