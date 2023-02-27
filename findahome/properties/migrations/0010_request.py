# Generated by Django 4.1.1 on 2022-11-23 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('properties', '0009_delete_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property')),
                ('reservation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.reservation')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]