from django.urls import path
from . import views

urlpatterns = [
    path('',views.login),
    path('login',views.get_login_data),
    path('data',views.data),
    path('getdata',views.get_data),
    path('gensetdeshboard',views.genset_deshboard),
    path('gensetreport', views.genset_report),
    path('gensetalarm', views.genset_alarm),
    path('logout', views.logout),
    path('inseruser', views.insert_user)
]
