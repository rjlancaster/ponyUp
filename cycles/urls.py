from django.conf.urls import url
from django.urls import path
from . import views

app_name = "cycles"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_user, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
]