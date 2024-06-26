# Generated by Django 3.2.19 on 2024-04-27 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TradingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('POSITIONS', 'Positions'), ('ORDERS', 'Orders'), ('FUND', 'Fund')], max_length=20)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('data', models.JSONField()),
                ('exp_brokerage', models.IntegerField()),
                ('order_count', models.IntegerField()),
                ('day_pl', models.IntegerField()),
            ],
        ),
    ]
