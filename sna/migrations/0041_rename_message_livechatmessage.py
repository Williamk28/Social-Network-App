# Generated by Django 4.1.3 on 2023-01-20 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sna', '0040_rename_value_message_message_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='LiveChatMessage',
        ),
    ]
