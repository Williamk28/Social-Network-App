# Generated by Django 4.1.3 on 2022-12-14 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sna', '0007_rename_diff_profile_userpost_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='diff_profile',
            field=models.BooleanField(default=False),
        ),
    ]
