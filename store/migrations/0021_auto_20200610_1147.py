# Generated by Django 3.0.6 on 2020-06-10 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20200610_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='customer/profile_pic/default_profile.png', null=True, upload_to='customer/profile_pic'),
        ),
    ]
