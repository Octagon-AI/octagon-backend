# Generated by Django 5.0.6 on 2024-07-06 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_aimodel_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='aimodel',
            name='accuracy',
            field=models.FloatField(null=True),
        ),
    ]
