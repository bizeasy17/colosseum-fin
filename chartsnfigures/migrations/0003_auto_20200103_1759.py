# Generated by Django 3.0 on 2020-01-03 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chartsnfigures', '0002_auto_20200102_2101'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='placeholder',
            options={'ordering': ['sequence'], 'verbose_name': '内容栏位', 'verbose_name_plural': '内容栏位'},
        ),
    ]
