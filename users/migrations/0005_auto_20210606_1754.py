# Generated by Django 3.2 on 2021-06-06 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210603_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='background_picture',
            field=models.ImageField(default='background_pictures/default_background_ulhcsp', upload_to='background_pictures/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/default_profile_djcnea', upload_to='profile_pictures/'),
        ),
    ]
