from django.db import models

# Create your models here.
from django.db import models

class TradingData(models.Model):
    CATEGORY_CHOICES = [
        ('POSITIONS', 'Positions'),
        ('ORDERS', 'Orders'),
        ('FUND', 'Fund')
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    last_updated = models.DateTimeField(auto_now=True)
    data = models.JSONField(null=True)
    exp_brokerage = models.IntegerField(null=True)
    order_count = models.IntegerField(null=True)
    day_pl = models.IntegerField(null=True)

from django.db import models

class TradingConfigurations(models.Model):
    default_stoploss = models.IntegerField(default=0)  # Field for default stoploss
    default_order_qty = models.IntegerField(default=0)  # Field for default order quantity
    max_loss = models.IntegerField(default=0)  # Field for maximum loss
    max_trade_count = models.IntegerField(default=0)  # Field for maximum trade count
    capital_usage_limit = models.IntegerField(default=0)  # Field for capital usage limit
    forward_trailing_points = models.IntegerField(default=0)  # Field for forward trailing points
    trailing_to_top_points = models.IntegerField(default=0)  # Field for trailing to top points
    reverse_trailing_points = models.IntegerField(default=0)  # Field for reverse trailing points
    stoploss_limit_slippage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    

    def __str__(self):
        return f"Trading Configurations - ID: {self.pk}"
