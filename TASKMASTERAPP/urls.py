from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Admin URLs (must come before default admin URL)
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/tasks/', views.admin_tasks, name='admin_tasks'),
    path('admin/feedback/', views.admin_feedback, name='admin_feedback'),
    path('admin/settings/', views.admin_settings, name='admin_settings'),
    path('admin/users/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),
    path('admin/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    
    # Default admin URL
    path('admin/', admin.site.urls),
    
    # Main URLs
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit-task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle-task/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/tasks/calendar/', views.calendar_events, name='calendar_events'),
    path('about/', views.about, name='about'),
    path('demo/', views.demo, name='demo'),
]
