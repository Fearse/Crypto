# Generated by Django 4.2 on 2023-04-29 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0002_cryptocoin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=7)),
                ('price', models.FloatField()),
                ('amount', models.IntegerField()),
                ('transType', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]
