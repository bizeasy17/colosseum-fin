from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'chartsnfigure'
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),
]
