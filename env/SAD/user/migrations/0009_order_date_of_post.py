# Generated by Django 2.2.4 on 2019-10-27 03:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_order_address_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date_of_post',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]