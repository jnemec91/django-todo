from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TodoList, TodoField, UserOptions

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        todo_lists = [{'name':i.name, 'owner':i.owner, 'fields':[a for a in i.fields.all()]} for i in TodoList.objects.filter(owner=request.user)]
        
        return render(request, 'todo_list/index.html', {'todo_lists':todo_lists})
    
    else:
        return redirect('todo_list_app:login')


def user_login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('todo_list_app:index')
        else:
            messages.add_message(request, messages.ERROR, 'You`ve entered a wrong username or password.')
            return redirect('todo_list_app:login')
   
    return render(request, 'todo_list/login.html')

def signup(request):
    return render(request, 'todo_list/signup.html')

@login_required
def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('todo_list_app:login')

