# Generated by Django 4.0.1 on 2022-01-17 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.ImageField(default='user-images/default.png', null=True, upload_to='user-images'),
        ),
    ]
