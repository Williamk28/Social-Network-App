# Generated by Django 4.1.3 on 2022-12-26 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sna', '0018_alter_customuser_interest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interesttag',
            old_name='interest',
            new_name='name',
        ),
    ]
