# administration/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create_admin/', views.create_admin, name='create_admin'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('add_time_slots/', views.add_time_slots, name='add_time_slots'),
    path('list_appointments/', views.list_appointments, name='list_appointments'),

    path('department/', views.department_list, name='department_list'),
    path('department/create/', views.department_create, name='department_create'),
    path('department/update/<int:pk>/', views.department_update, name='department_update'),
    path('department/delete/<int:pk>/', views.department_delete, name='department_delete'),
    path('add_doctor/<int:department_id>/', views.add_doctor, name='add_doctor'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_registration/', views.user_registration, name='user_registration'),
    
]
