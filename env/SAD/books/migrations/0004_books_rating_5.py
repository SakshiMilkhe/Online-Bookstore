# Generated by Django 2.2.4 on 2019-08-30 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20190813_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='rating_5',
            field=models.IntegerField(default=0),
        ),
    ]
