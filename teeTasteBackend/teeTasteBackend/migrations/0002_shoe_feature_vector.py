# Generated by Django 4.2.3 on 2023-07-30 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teeTasteBackend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='feature_vector',
            field=models.TextField(blank=True, null=True),
        ),
    ]
