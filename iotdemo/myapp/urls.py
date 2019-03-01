from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('sub', views.subscribe),
    path('pubon', views.publish_on),
    path('puboff', views.publish_off),
    path('postdata',views.check_data),
    path('postdatatest',views.check_data_test)
]

