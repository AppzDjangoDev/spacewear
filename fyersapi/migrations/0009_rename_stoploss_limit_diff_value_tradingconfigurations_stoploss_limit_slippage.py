# Generated by Django 3.2.19 on 2024-05-02 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fyersapi', '0008_rename_trailingtotop_points_tradingconfigurations_trailing_to_top_points'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tradingconfigurations',
            old_name='stoploss_limit_diff_value',
            new_name='stoploss_limit_slippage',
        ),
    ]
