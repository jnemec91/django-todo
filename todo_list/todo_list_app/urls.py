from django.urls import path
from . import views
import django.contrib.auth.views as auth_views


app_name = 'todo_list_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.log_out, name='logout'),\
    path('create_todo_list/', views.create_todo_list, name='create_todo_list'),
    path('edit_todo_list/<int:todo_list_id>/', views.edit_todo_list, name='edit_todo_list'),
    path('delete_todo_list/<int:todo_list_id>/', views.delete_todo_list, name='delete_todo_list'),
    path('list_of_todo_lists/', views.list_of_todo_lists, name='list_of_todo_lists'),
    path('todo_list/<str:todo_list_hash>/', views.list_details, name='list_details'),
    path('check/<int:todo_field_id>',views.check_task, name='check_task'),
    path('settings/', views.settings, name='settings'),
    path('add_to_my_list/<int:todo_list_id>/', views.add_to_my_list, name='add_to_my_list'),


    path('password_reset/', views.ToDoAppPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.ToDoAppPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.ToDoAppPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.ToDoAppPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
