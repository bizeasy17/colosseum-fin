from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^$', views.UserListView.as_view(), name='list'),
    url(r'^~redirect/$', views.UserRedirectView.as_view(), name='redirect'),
    url(r'^~update/$', views.UserUpdateView.as_view(), name='update'),
    url(r'^(?P<username>[\w.@+-]+)/$',
        views.UserDetailView.as_view(), name='detail'),
]
