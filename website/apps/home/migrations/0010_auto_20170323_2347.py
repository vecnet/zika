# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 03:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_totals_for_existing_sims'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date',
            field=models.DateField(db_index=True),
        ),
    ]
