# Generated by Django 5.0.1 on 2024-08-13 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_delete_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='safe_level',
            field=models.IntegerField(default=10),
        ),
    ]
