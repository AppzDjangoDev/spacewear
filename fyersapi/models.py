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
