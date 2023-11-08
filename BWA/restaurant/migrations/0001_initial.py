# Generated by Django 4.0.4 on 2023-11-08 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raison_sociale', models.CharField(max_length=100)),
                ('addresse', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField()),
            ],
        ),
    ]
