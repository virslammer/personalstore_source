# Generated by Django 3.0.6 on 2020-06-10 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20200610_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='customer-profile-pic'),
        ),
    ]
