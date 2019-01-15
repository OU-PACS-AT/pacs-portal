# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-12-10 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scaffold', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated_by', models.CharField(default=None, max_length=8)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default=None, max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course_id', models.IntegerField()),
                ('assignment_number', models.IntegerField(unique=True)),
                ('assignment_name', models.CharField(max_length=100)),
                ('start_date', models.CharField(max_length=10)),
                ('due_date', models.CharField(max_length=10)),
                ('end_date', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
