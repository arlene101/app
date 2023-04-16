from django.urls import re_path
from backend_api import views

urlpatterns=[
    re_path(r'^courier$',views.courierApi),
    re_path(r'^con$',views.conApi),
    re_path(r'^order$',views.addCourierOrder),
    re_path(r'^createuser$',views.create_user),
    re_path(r'^couriersms$',views.courierSms),
]