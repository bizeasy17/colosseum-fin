from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import TradeRec

STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)

MARKET_CHOICE = (
    ('sh', _('上海')),
    ('sz', _('深圳')),
)

TRADE_DIRECTION = (
    ('b', _('买入')),
    ('s', _('卖出')),
)

TRADE_FLAG = (
    ('s', _('首次建仓')),
    ('n', _('正常买入/卖出')),
    ('f', _('清仓')),
)


class TradeRecForm(forms.ModelForm):
    # market = forms.ChoiceField(label=_('交易市场'), choices=MARKET_CHOICE)
    # stock_name = forms.CharField(label=_('股票名称'),
    #     widget=forms.TextInput(attrs={'placeholder': _('譬如: 万科a')}))
    # stock_code = forms.CharField(label=_('股票名称'),
    #     widget=forms.TextInput(attrs={'placeholder': _('譬如: 000001')}))
    # strategy = forms.CharField(label=_('操作策略'))
    # direction = forms.ChoiceField(label=_('交易类型'), choices=TRADE_DIRECTION)
    # flag = forms.ChoiceField(label=_('交易标签'), choices=TRADE_FLAG)
    # price = forms.FloatField(label=_('交易价格'))
    # cash = forms.FloatField(label=_('交易金额'))
    # position = forms.CharField(label=_('仓位'))

    class Meta:
        model = TradeRec
        # exclude = ['created_time', 'last_mod_time', 'pub_time', 'market',
        #            'featured_image', 'author', 'views', 'comment_status']
        fields = ['author', 'market', 'stock_name', 'stock_code', 'strategy',
                  'direction', 'trade_time', 'flag', 'price', 'cash', 'position', ]
        labels = {
            'stock_name': _('股票名称或代码'),
        }


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
