"""colosseum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('admin/', admin.site.urls),

    # User management
    
    url(r'^users/', include('users.urls')),
    url(r'^accounts/', include('allauth.urls')),

    # Local apps here
    # path('report/', include('chartsnfigures.urls')), # home page
    url(r'', include('chartsnfigures.urls', namespace='chartsnfigures')),
    path('traderec/', include('traderec.urls')),
    path('notifications/', include('notifications.urls')),

    # 3rd Party Apps
    url(r'mdeditor/', include('mdeditor.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
