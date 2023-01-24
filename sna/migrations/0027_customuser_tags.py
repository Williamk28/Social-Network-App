# Generated by Django 4.1.3 on 2023-01-08 15:22

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('sna', '0026_likeuserpost_userpost_no_of_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
