# Generated by Django 3.2.10 on 2022-01-20 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220112_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='venue_price',
        ),
    ]
