# Generated by Django 2.2.3 on 2019-09-10 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_trip_competition'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='end_point',
            field=models.IntegerField(default=0),
        ),
    ]