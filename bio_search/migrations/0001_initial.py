# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportDatabase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userpwd', models.CharField(max_length=20, verbose_name=b'password')),
                ('iterm_number', models.CharField(unique=True, max_length=20, verbose_name=b'number')),
                ('iterm_report_name', models.CharField(max_length=30, verbose_name=b'report')),
                ('iterm_path', models.CharField(max_length=100, verbose_name=b'path')),
                ('iterm_type', models.CharField(max_length=1, verbose_name=b'type', choices=[(b'R', b'RNA-Seq with reference'), (b'D', b'RNA-Seq without reference'), (b'M', b'microRNA'), (b'C', b'Chip-Seq')])),
                ('iterm_stime', models.DateTimeField()),
                ('iterm_ftime', models.DateTimeField()),
                ('iterm_status', models.CharField(max_length=1, verbose_name=b'status', choices=[(b'U', b'Under way'), (b'P', b'Postpone'), (b'F', b'Finshed')])),
                ('iterm_memo', models.TextField()),
                ('username', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Report',
            },
            bases=(models.Model,),
        ),
    ]
