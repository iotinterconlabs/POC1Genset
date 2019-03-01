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
    path('transfdeshboard',views.transf_deshboard),
    path('transfreport', views.transf_report),
    path('transfalarm', views.transf_alarm),
    path('gascdeshboard',views.gasc_deshboard),
    path('gascreport', views.gasc_report),
    path('gascalarm', views.gasc_alarm),
    path('watermdeshboard',views.waterm_deshboard),
    path('watermreport', views.waterm_report),
    path('watermalarm', views.waterm_alarm),
    path('logout', views.logout),
    path('inseruser', views.insert_user),
    path('getlog', views.get_log)
]
