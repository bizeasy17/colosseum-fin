from django import forms
from .models import TradeRec

class TradeRecForm(forms.ModelForm):
    # body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = TradeRec
        fields = '__all__'