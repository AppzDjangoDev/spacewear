# Generated by Django 3.2.19 on 2024-04-28 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyersapi', '0002_auto_20240427_0759'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradingConfigurations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_stoploss', models.IntegerField(default=0)),
                ('default_order_qty', models.IntegerField(default=0)),
                ('max_loss', models.IntegerField(default=0)),
                ('max_trade_count', models.IntegerField(default=0)),
                ('capital_usage_limit', models.IntegerField(default=0)),
            ],
        ),
    ]
