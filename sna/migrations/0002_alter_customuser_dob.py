# Generated by Django 4.1.3 on 2022-12-05 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sna', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='dob',
            field=models.DateField(null=True),
        ),
    ]