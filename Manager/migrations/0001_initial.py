# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 20:42
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attrs', django.contrib.postgres.fields.jsonb.JSONField()),
                ('catagory', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
