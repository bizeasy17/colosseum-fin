# Generated by Django 3.0 on 2020-01-15 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traderec', '0005_auto_20200115_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocknamecodemap',
            name='stock_code',
            field=models.CharField(max_length=50, unique=True, verbose_name='股票代码'),
        ),
        migrations.AlterField(
            model_name='stocknamecodemap',
            name='stock_name',
            field=models.CharField(max_length=50, unique=True, verbose_name='股票名称'),
        ),
    ]
