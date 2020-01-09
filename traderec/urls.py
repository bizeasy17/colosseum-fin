from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'traderec'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    url(r'^create-new-traderec/$', views.TradeRecCreateView.as_view(), name='create_new'),

    # path(r'create', views.TradeRecCreateView.as_view(), name='create'),
    path('update', views.TradeRecUpdateView.as_view(), name='update'),
    path('history', views.TradeRecHistoryView.as_view(), name='history'),

    path(r'<int:year>/<int:month>/<int:day>/<int:traderec_id>',
         views.TradeRecDetailView.as_view(),
         name='detailbyid'),

    # sample form
    path('form', views.get_name),
    
]
