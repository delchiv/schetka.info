# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20150102_2007'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
