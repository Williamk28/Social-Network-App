# Generated by Django 4.1.3 on 2023-01-08 16:39

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('sna', '0027_customuser_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
