# Generated by Django 2.2.1 on 2019-06-18 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='respondent',
            field=models.TextField(blank=True, null=True),
        ),
    ]
