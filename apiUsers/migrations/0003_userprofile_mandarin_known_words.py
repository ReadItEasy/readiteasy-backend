# Generated by Django 3.0.3 on 2020-04-05 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiUsers', '0002_auto_20200403_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='mandarin_known_words',
            field=models.TextField(blank=True, default=''),
        ),
    ]