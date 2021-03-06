# Generated by Django 3.0.6 on 2020-06-02 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20200527_0011'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='city',
            new_name='phone',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='state',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
