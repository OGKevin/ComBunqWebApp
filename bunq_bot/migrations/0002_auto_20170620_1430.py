# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-20 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bunq_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BunqNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('author', models.CharField(blank=True, max_length=150, null=True)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TogetherUpdates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='botinfo',
            name='news_titles',
        ),
        migrations.RemoveField(
            model_name='botinfo',
            name='together_titles',
        ),
    ]
