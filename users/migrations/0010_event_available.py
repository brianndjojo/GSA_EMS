# Generated by Django 3.2.10 on 2022-01-20 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_venue_venue_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]