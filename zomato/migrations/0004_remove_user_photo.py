# Generated by Django 2.2.3 on 2019-07-13 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zomato', '0003_auto_20190713_0629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='photo',
        ),
    ]
