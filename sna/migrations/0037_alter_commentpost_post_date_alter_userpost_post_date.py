# Generated by Django 4.1.3 on 2023-01-19 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sna', '0036_alter_customuser_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentpost',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
