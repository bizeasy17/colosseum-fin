# Generated by Django 3.0.2 on 2020-01-19 03:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('traderec', '0008_auto_20200116_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='positions',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='持仓人'),
        ),
        migrations.AddField(
            model_name='positions',
            name='is_liquadated',
            field=models.CharField(db_index=True, default='n', editable=False, max_length=1, verbose_name='是否清仓'),
        ),
        migrations.AddField(
            model_name='traderec',
            name='stock_positions_master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='traderec.Positions', verbose_name='股票持仓'),
        ),
        migrations.AlterField(
            model_name='traderec',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='traderec',
            name='flag',
            field=models.CharField(blank=True, choices=[('s', '首次建仓'), ('n', '正常买入/卖出'), ('l', '清仓')], default='b', max_length=1, null=True, verbose_name='交易标签'),
        ),
        migrations.AlterField(
            model_name='traderec',
            name='is_deleted',
            field=models.CharField(default='n', editable=False, max_length=1, verbose_name='是否被删除'),
        ),
        migrations.AlterField(
            model_name='traderec',
            name='position',
            field=models.CharField(max_length=50, verbose_name='本次交易仓位'),
        ),
    ]
