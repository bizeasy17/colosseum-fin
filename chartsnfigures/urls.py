from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'chartsnfigure'
urlpatterns = [
    path(r'', views.IndexView.as_view(), name='index'),

    path(r'page/<int:page>/', views.IndexView.as_view(), name='index_page'),

#     path(r'report/<slug:slug>',
#          views.CNFReportDetailView.as_view(),
#          name='detailbyslug'),
    url(r'^(?P<slug>[-\w]+)/$', views.CNFReportDetailView.as_view(), name='report'),
     

    path(r'report/<int:year>/<int:month>/<int:day>/<int:report_id>.html',
         views.CNFReportListView.as_view(),
         name='detailbyid'),

    path(r'category/<slug:category_name>.html',
         views.CategoryDetailView.as_view(), name='category_detail'),
    path(r'category/<slug:category_name>/<int:page>.html', views.CategoryDetailView.as_view(),
         name='category_detail_page'),

    path(r'author/<author_name>.html',
         views.AuthorDetailView.as_view(), name='author_detail'),
    path(r'author/<author_name>/<int:page>.html', views.AuthorDetailView.as_view(),
         name='author_detail_page'),

    path(r'tag/<slug:tag_name>.html',
         views.TagDetailView.as_view(), name='tag_detail'),
    path(r'tag/<slug:tag_name>/<int:page>.html',
         views.TagDetailView.as_view(), name='tag_detail_page'),
    # path('archives.html', cache_page(60 * 60)(views.ArchivesView.as_view()), name='archives'),
    # path('links.html', views.LinkListView.as_view(), name='links'),
    # path(r'upload', views.fileupload, name='upload'),
    # path(r'refresh', views.refresh_memcache, name='refresh'),
]
