from django.urls import path
from core.views import no_permission,home

urlpatterns = [
    path("no-permission/",no_permission,name='no_permission'),
    path("",home,name="home"),
]