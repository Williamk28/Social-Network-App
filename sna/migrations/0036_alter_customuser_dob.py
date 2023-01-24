# Generated by Django 4.1.3 on 2023-01-19 16:25

from django.db import migrations, models
import sna.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sna', '0035_userpost_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='dob',
            field=models.DateField(validators=[sna.validators.AgeValidator(16)]),
        ),
    ]
