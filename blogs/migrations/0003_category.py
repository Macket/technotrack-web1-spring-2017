# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20170324_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('blogs', models.ManyToManyField(to='blogs.Blog')),
            ],
        ),
    ]
