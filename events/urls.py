from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
  
    
    path('category-list/',category_list,name='category_list'),
    path('category/create/', add_category, name='add_category'),
    path('category/update/<int:id>/', update_category, name='update_category'),
    path('category/delete/<int:id>/', delete_category, name='delete_category'),
    # path('<int:id>/',event_detail, name='event_detail'),
    path('rsvp/<int:id>/',rsvp_event,name="rsvp_event"),
    path('create/', event_create, name='event_create'),
    path('update/<int:id>/', event_update, name='event_update'),
    path('delete/<int:id>/', event_delete, name='event_delete'),
    path('event-list/',event_list,name="event_list"),
    path('participants/', participant_list, name='participant_list'),
    # path('participants/create/', participant_create, name='participant_create'),
    path('participants/delete/<int:id>',delete_participant, name='delete_participant'),
    path('dashboard/', dashboard, name='dashboard'),
    path('organizer/dashboard/', organizer_dashboard, name='organizer_dashboard'),
    path('participant/dashboard/', participant_dashboard, name='participant_dashboard'),
    
]