# Generated by Django 2.2.3 on 2019-07-28 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='road',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]