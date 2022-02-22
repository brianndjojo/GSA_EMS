# Generated by Django 3.2.10 on 2022-01-12 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20220112_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='signup',
            name='attachments',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='signup',
            name='description',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
    ]