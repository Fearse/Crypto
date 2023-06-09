# Generated by Django 4.2 on 2023-04-29 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0003_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocoin',
            name='image_url',
            field=models.CharField(default='123', max_length=100),
        ),
        migrations.AlterField(
            model_name='cryptocoin',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(),
        ),
    ]
