# Generated by Django 3.0.3 on 2020-04-23 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiWords', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mandarinword',
            name='hsk',
            field=models.IntegerField(default=7),
        ),
        migrations.AddField(
            model_name='mandarinword',
            name='pronunciation_num',
            field=models.CharField(max_length=80, null=True),
        ),
    ]