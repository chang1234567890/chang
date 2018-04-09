# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('hcontent', tinymce.models.HTMLField()),
            ],
        ),
    ]
