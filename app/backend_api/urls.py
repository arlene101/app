from django.urls import re_path
from backend_api import views

urlpatterns=[
    re_path(r'^courier$',views.courierApi),

    re_path(r'^order$',views.addCourierOrder),
]