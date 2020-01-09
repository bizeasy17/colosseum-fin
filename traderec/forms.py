from django import forms
from .models import TradeRec

STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)


class TradeRecForm(forms.ModelForm):
    # email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    # password = forms.CharField(widget=forms.PasswordInput())
    # address_1 = forms.CharField(
    #     label='Address',
    #     widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    # )
    # address_2 = forms.CharField(
    #     widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
    # )
    # city = forms.CharField()
    # state = forms.ChoiceField(choices=STATES)
    # zip_code = forms.CharField(label='Zip')
    # check_me_out = forms.BooleanField(required=False)

    class Meta:
        model = TradeRec
        # exclude = ['created_time', 'last_mod_time', 'pub_time', 'market',
        #            'featured_image', 'author', 'views', 'comment_status']
        fields = ['stock_name', 'stock_code', 'direction', 'flag', 'price', 'cash', 'position', 'strategy']


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
