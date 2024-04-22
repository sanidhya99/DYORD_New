# Generated by Django 4.2.3 on 2023-12-28 01:34

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=100, null=True)),
                ('source', models.CharField(max_length=100)),
                ('destination', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('startTime', models.TimeField()),
                ('endTime', models.TimeField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('purpose', models.CharField(default='Daily Life Travelling', max_length=100)),
            ],
        ),
    ]
