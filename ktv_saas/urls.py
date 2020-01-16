"""ktv_saas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/(?P<version>[v1|v2]+)/db_module/', include('db_module.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/buy_and_sell/', include('buy_and_sell.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/inventory/', include('inventory.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/member/', include('member.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/merchant_file/', include('merchant_file.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/products/', include('products.urls')),
    url(r'^api/(?P<version>[v1|v2]+)/report/', include('report.urls')),
    path('media/<path:path>',serve,{'document_root':settings.MEDIA_ROOT}),
]
