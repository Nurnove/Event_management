from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('<int:id>/',event_detail, name='event_detail'),
    path('create/', event_create, name='event_create'),
    path('update/<int:id>/', event_update, name='event_update'),
    path('delete/<int:id>/', event_delete, name='event_delete'),

    path('event/participants/', participant_list, name='participant_list'),
    path('event/participants/create/', participant_create, name='participant_create'),

    path('dashboard/', dashboard, name='dashboard'),
]