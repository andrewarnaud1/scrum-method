# Generated by Django 4.0.4 on 2023-11-08 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_adresse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='addresse',
        ),
    ]