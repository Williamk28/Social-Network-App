# Generated by Django 4.1.3 on 2023-01-01 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sna', '0020_message_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='staff',
            field=models.BooleanField(default=False),
        ),
    ]