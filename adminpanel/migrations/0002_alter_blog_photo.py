# Generated by Django 3.2 on 2021-05-01 16:49

import adminpanel.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='photo',
            field=models.FileField(default='background.jpeg', upload_to='blogs/', validators=[adminpanel.models.validate_file_size]),
        ),
    ]
