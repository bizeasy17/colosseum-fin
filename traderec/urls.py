from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = 'traderec'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('users/<username>/home', views.IndexView.as_view(), name='home'),

    path('create', views.TradeRecCreateView.as_view(), name='create_new'),
    path('update', views.TradeRecUpdateView.as_view(), name='update'),
    path('history', views.TradeRecHistoryView.as_view(), name='history'),

    path('stocks/realtime_quote/<ts_code>', views.get_realtime_quotes, name='get_realtime_quote'),
    path('stocks/code/<stock_name>', views.get_stockcode_by_name, name='get_stockcode'),
    path('stocks/name/<stock_code>', views.get_stockname_by_code, name='get_stockname'),
    path('stocks/kline/code/<ts_code>/startdate/<start_date>/enddate/<end_date>', views.get_stock_kline_ext, name='get_kline'),

    path(r'<int:year>/<int:month>/<int:day>/<int:traderec_id>',
         views.TradeRecDetailView.as_view(),
         name='detailbyid'),

    # sample form
    path('form/<ts_code>', views.get_name, name='sample'),
    
]
