# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-07-30 02:44


import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('reason', models.TextField()),
                ('start', models.DateTimeField(default=datetime.datetime.now)),
                ('end', models.DateTimeField()),
                ('permenant', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_bans', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bans', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('can_ban', 'Can ban users'),),
            },
        ),
    ]
