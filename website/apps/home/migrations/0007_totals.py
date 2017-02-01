# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 21:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_simulation_is_uploaded'),
    ]

    operations = [
        migrations.CreateModel(
            name='Totals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_date', models.DateField()),
                ('total_low', models.FloatField()),
                ('total_mid', models.FloatField(blank=True, null=True)),
                ('total_high', models.FloatField(blank=True, null=True)),
                ('date_output_generated', models.DateField(blank=True, null=True)),
                ('simulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='totals_data', to='home.Simulation')),
            ],
        ),
    ]
