# Generated by Django 4.0.5 on 2022-08-03 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_rename_voucher_voucherlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock_item',
            name='opening_balance',
        ),
    ]
