# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-10 21:58
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20181010_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='goal_mark',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(100.0), django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='weight',
            field=models.FloatField(null=True, validators=[django.core.validators.MaxValueValidator(100.0), django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
