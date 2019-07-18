from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^stock/$',views.stock_pool_show),
    # url(r'^$',views.fund_show),
    url(r'^fund/$', views.fund_show),
    url(r'^linian/$', views.linian_show),
    url(r'^fundold/$', views.fundold_show),
    url(r'^download/$', views.downdata_from_carxiuli),



]
