# Generated by Django 4.2 on 2023-04-29 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_user_delete_user1'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
