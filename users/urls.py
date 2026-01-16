from django.urls import path,include
from users.views import sign_in,sign_out,sign_up,assign_role,create_group,activate_user,admin_dashboard


urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='logout'),
    path('activate/<int:id>/<str:token>/', activate_user),
    path('admin/assign-role/<int:id>', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create_group'),
    path("admin/dashboard/",admin_dashboard,name="admin_dashboard"),
    
    
]