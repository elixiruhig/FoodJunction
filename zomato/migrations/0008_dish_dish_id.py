# Generated by Django 2.2.3 on 2019-07-13 11:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('zomato', '0007_hotel_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='dish_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
