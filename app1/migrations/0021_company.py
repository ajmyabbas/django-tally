# Generated by Django 4.0.5 on 2022-08-12 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0020_alter_stock_item_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_name', models.CharField(max_length=100, null=True)),
                ('start_date', models.DateField()),
            ],
        ),
    ]
