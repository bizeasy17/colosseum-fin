from django import forms
from .models import CNFReport

class CNFReportForm(forms.ModelForm):
    # body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = CNFReport
        fields = '__all__'