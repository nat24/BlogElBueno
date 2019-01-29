from django.conf.urls import url
from django.contrib import admin
from .views import autor


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', autor,name="detail"),
    
]