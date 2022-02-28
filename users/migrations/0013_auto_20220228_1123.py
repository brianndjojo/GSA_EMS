# Generated by Django 3.2.10 on 2022-02-28 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_rfid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rfid',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='rfid',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
