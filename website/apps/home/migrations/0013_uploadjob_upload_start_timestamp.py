# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-25 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20170325_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadjob',
            name='upload_start_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]