# Generated by Django 3.0.7 on 2020-08-20 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_movie_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='averageRating',
            field=models.FloatField(default=0),
        ),
    ]
