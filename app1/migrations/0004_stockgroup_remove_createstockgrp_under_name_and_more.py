# Generated by Django 4.0.5 on 2022-07-30 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_rename_per_stock_item_rateper_remove_stock_item_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grp_name', models.CharField(max_length=70)),
            ],
        ),
        migrations.RemoveField(
            model_name='createstockgrp',
            name='under_name',
        ),
        migrations.AddField(
            model_name='createstockgrp',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.stockgroup'),
        ),
    ]
