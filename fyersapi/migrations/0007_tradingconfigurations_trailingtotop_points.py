# Generated by Django 3.2.19 on 2024-05-02 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fyersapi', '0006_alter_tradingconfigurations_stoploss_limit_diff_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradingconfigurations',
            name='trailingtotop_points',
            field=models.IntegerField(default=0),
        ),
    ]
