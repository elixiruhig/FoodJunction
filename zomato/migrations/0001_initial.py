# Generated by Django 2.2.3 on 2019-07-13 06:02

import datetime
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('name', models.CharField(max_length=255)),
                ('item_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('price', models.IntegerField()),
                ('veg', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Items',
                'verbose_name': 'Item',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('user_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone', models.BigIntegerField(max_length=13)),
                ('category', models.CharField(default='Customer', max_length=255)),
                ('sector', models.IntegerField()),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('photo', models.ImageField(null=True, upload_to='group_photos')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedMenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zomato_taggedmenuitem_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zomato_menuitem_items', to='zomato.MenuItem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='zomato.TaggedMenuItem', to='zomato.MenuItem', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sector', models.IntegerField()),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zomato.Menu')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zomato.User')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('price', models.IntegerField()),
                ('time', models.DateTimeField(default=datetime.datetime(2019, 7, 13, 6, 2, 19, 865819))),
                ('duration', models.IntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zomato.User')),
                ('ordered_items', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='zomato.TaggedMenuItem', to='zomato.MenuItem', verbose_name='Tags')),
            ],
        ),
    ]