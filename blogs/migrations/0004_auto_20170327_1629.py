# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', 'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='blogs',
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ManyToManyField(related_name='category_blog', to='blogs.Category'),
        ),
    ]
