# Generated by Django 3.2.19 on 2024-05-02 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fyersapi', '0007_tradingconfigurations_trailingtotop_points'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tradingconfigurations',
            old_name='trailingtotop_points',
            new_name='trailing_to_top_points',
        ),
    ]