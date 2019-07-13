"""Zomato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Zomato import settings
from zomato import views
app_name = 'zomato'
urlpatterns = [
    path('',views.homeview,name='homeview'),
    path('user_login/',views.user_login, name = 'user_login'),
    path('user_logout/',views.user_logout, name = 'user_logout'),
    path('register/',views.register, name = 'register'),
    url(r'^hotel=(?P<hotel_id>[-\w]+)/$',views.hotelview, name = 'hotelview'),
    url(r'^cart=(?P<user_id>[-\w]+)/$',views.cartview, name = 'cartview'),

]
if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
