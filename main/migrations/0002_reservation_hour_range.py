# Generated by Django 5.2.1 on 2025-05-25 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='hour_range',
            field=models.CharField(default='12:00 - 13:00', max_length=20),
            preserve_default=False,
        ),
    ]
