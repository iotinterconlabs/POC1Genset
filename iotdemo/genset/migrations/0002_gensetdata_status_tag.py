# Generated by Django 2.0.5 on 2018-08-16 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genset', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gensetdata',
            name='status_tag',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
