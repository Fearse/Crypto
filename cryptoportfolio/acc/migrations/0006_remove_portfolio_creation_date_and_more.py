# Generated by Django 4.2 on 2023-05-20 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0005_remove_cryptocoin_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='date',
        ),
    ]
