# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-14 23:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160514_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackmodel',
            name='track_rating',
            field=models.CharField(blank=True, choices=[('1', '1 star'), ('2', '2 stars'), ('3', '3 stars'), ('4', '4 stars'), ('5', '5 stars')], max_length=10),
        ),
    ]
