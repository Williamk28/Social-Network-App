# Generated by Django 4.1.3 on 2022-12-21 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sna', '0016_remove_interesttag_user_customuser_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interesttag',
            name='interest',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
