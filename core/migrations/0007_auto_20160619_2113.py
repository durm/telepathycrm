# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-19 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_circulation_document_meeting_note_phonecall_project_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='skype',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='skype'),
        ),
        migrations.AlterField(
            model_name='document',
            name='attach',
            field=models.FileField(upload_to='attachs/documents', verbose_name='вложение'),
        ),
        migrations.AlterField(
            model_name='note',
            name='attach',
            field=models.FileField(blank=True, null=True, upload_to='attachs/notes', verbose_name='вложение'),
        ),
    ]
