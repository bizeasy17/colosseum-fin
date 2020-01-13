from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = 'traderec'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('create', views.TradeRecCreateView.as_view(), name='create_new'),
    path('endpoint/realtime-quotes/<ts_code>', views.get_realtime_quotes, name='realtime_quotes'),
    path('endpoint/stockcode/<stock_name>', views.get_stockcode, name='get_stockcode'),
    path('endpoint/stockname/<stock_code>', views.get_stockname, name='get_stockname'),

    path('endpoint/stock_kline/<ts_code>/<start_date>/<end_date>', views.get_stock_kline, name='get_kline'),

    path('update', views.TradeRecUpdateView.as_view(), name='update'),
    path('history', views.TradeRecHistoryView.as_view(), name='history'),

    path(r'<int:year>/<int:month>/<int:day>/<int:traderec_id>',
         views.TradeRecDetailView.as_view(),
         name='detailbyid'),

    # sample form
    path('form/<ts_code>', views.get_name, name='sample'),
    
]
