from django import forms
from .models import TradingConfigurations

class TradingConfigurationsForm(forms.ModelForm):
    class Meta:
        model = TradingConfigurations
        fields = '__all__'  # To include all fields from the model
        # Alternatively, you can specify the fields explicitly:
        # fields = ['default_stoploss', 'default_order_qty', 'max_loss', 'max_trade_count', 'capital_usage_limit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add classes to form fields for Bootstrap styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'