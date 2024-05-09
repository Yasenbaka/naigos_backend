# Generated by Django 5.0.4 on 2024-05-09 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_appid', models.BigIntegerField()),
                ('access_token', models.TextField()),
                ('refresh_token', models.TextField()),
                ('safe_level', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qq_id', models.BigIntegerField()),
                ('register_group', models.BigIntegerField()),
                ('nickname', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('score', models.IntegerField(default=0)),
                ('favorite', models.IntegerField(default=0)),
                ('avatar', models.URLField()),
                ('channel_user_id', models.CharField(max_length=255)),
            ],
        ),
    ]