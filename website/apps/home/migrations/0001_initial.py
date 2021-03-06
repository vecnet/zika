# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateField(default='1999-01-01')),
                ('location', models.TextField(default='')),
                ('department', models.TextField(default='')),
                ('municipality', models.TextField(default='')),
                ('data_type', models.TextField(default='')),
                ('data_field_code', models.TextField(default='')),
                ('value', models.IntegerField(default=0)),
            ],
        ),
    ]
