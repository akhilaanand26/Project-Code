# Generated by Django 4.1.1 on 2022-11-23 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_remove_property_image1_request'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Request',
        ),
    ]
