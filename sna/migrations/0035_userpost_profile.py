# Generated by Django 4.1.3 on 2023-01-19 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sna', '0034_remove_userpost_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='profile',
            field=models.CharField(default='Admin', max_length=50),
            preserve_default=False,
        ),
    ]