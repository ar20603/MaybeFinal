# Generated by Django 2.1.1 on 2018-09-01 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='lastTime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='match',
            name='time1',
            field=models.IntegerField(default=900),
        ),
        migrations.AddField(
            model_name='match',
            name='time2',
            field=models.IntegerField(default=900),
        ),
    ]
