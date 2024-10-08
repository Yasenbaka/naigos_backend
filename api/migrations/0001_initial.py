# Generated by Django 5.0.3 on 2024-08-15 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SogouInputTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(blank=True, null=True)),
                ('introduce', models.TextField(blank=True, null=True)),
                ('header_image', models.URLField(blank=True, null=True)),
                ('details_image', models.URLField(blank=True, null=True)),
                ('cost', models.IntegerField(default=100)),
            ],
        ),
    ]
