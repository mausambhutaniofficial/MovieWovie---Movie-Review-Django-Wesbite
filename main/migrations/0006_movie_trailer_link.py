# Generated by Django 3.0.7 on 2020-08-25 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer_link',
            field=models.URLField(default=None, null=True),
        ),
    ]