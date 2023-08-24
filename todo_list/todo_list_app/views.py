from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'todo_list/index.html')

def login(request):
    return render(request, 'todo_list/login.html')

def signup(request):
    return render(request, 'todo_list/signup.html')

def logout(request):
    return render(request, 'todo_list/logout.html')

