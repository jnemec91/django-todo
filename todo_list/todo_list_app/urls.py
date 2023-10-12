from django.urls import path
from . import views

app_name = 'todo_list_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.log_out, name='logout')
]
