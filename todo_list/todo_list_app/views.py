from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .models import TodoList, TodoField, UserOptions
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView 

# Create your views here.

def index(request):
    """
    View function for home page of site. 
    
    If user is authenticated, returns list of todo lists.

    If user isnt authenticated redirects to login page.
    """
    if request.user.is_authenticated:
        todo_lists = [
            {
                'id':i.id,
                'name':i.name,
                'owner':i.owner,
                'fields':[a for a in i.fields.all()],
                'hash':i.hash,
            } 
            for i in TodoList.objects.filter(owner=request.user).order_by('-created_at')
        ]     
        
        return render(request, 'todo_list/index.html', {'todo_lists':todo_lists})
    
    else:
        return redirect('todo_list_app:login')

def list_details(request, todo_list_hash: str):
        """
        View function for todo list details page.
        
        Returns todo list details.
        
        Todo list hash is used to get todo list and is required parameter.
        """
        todo_lists = [
            {
                'id':i.id,
                'name':i.name,
                'owner':i.owner,
                'fields':[a for a in i.fields.all()],
                'hash':i.hash,
            } 
            for i in TodoList.objects.filter(hash=todo_list_hash)
        ]
        
        return render(request, 'todo_list/detail.html', {'todo_lists':todo_lists})



def user_login(request):
    """
    View function for login page.

    If user is authenticated, redirects to index page.

    If user is not authenticated, returns login page.
    """
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('todo_list_app:index')
        else:
            messages.add_message(request, messages.ERROR, 'You`ve entered a wrong username or password.')

            return redirect('todo_list_app:login')
        

    elif request.user.is_authenticated:
        return redirect('todo_list_app:index')
    
    return render(request, 'todo_list/login.html')


def signup(request):
    """
    View function for signup page.

    If user is authenticated, redirects to index page.

    If user is not authenticated, returns signup page.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')    
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.ERROR, 'This username already exists.')
                
                return redirect('todo_list_app:signup')
            
            elif User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR, 'Account with this email already exists.')

                return redirect('todo_list_app:signup')
            
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                user_options = UserOptions.objects.create(user=user)
                user_options.dark_mode = False
                user_options.email_notifications = False
                user_options.save()

                return redirect('todo_list_app:login')
                
        else:
            messages.add_message(request, messages.ERROR, 'Passwords do not match.')

            return redirect('todo_list_app:signup')

    elif request.user.is_authenticated:

        return redirect('todo_list_app:index')
    
    
    return render(request, 'todo_list/signup.html')


@login_required
def log_out(request):
    """
    Logout function.

    Logs out user and redirects to login page.
    """
    logout(request)
    
    return redirect('todo_list_app:login')


@login_required
def create_todo_list(request):
    """
    Create todo list page view.

    If method is POST, creates todo list and redirects to index page. 

    If method is GET, returns create todo list page.
    """
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        new_fields = request.POST.getlist('fields_new')
        new_descriptions = request.POST.getlist('descriptions_new')
        new_deadlines = request.POST.getlist('deadlines_new')
        shared = request.POST.get('is-shared')
        new_deadlines = [i if i != '' else None for i in new_deadlines]
        todo_list = TodoList.objects.create(name=name, owner=request.user, access_granted=shared)
        todo_list.hash = todo_list._create_hash()
        todo_list.save()
        if new_fields:
            for c,i in enumerate(new_fields):
                field = TodoField.objects.create(name=i, text=new_descriptions[c], checked=False, deadline_at=new_deadlines[c])
                field.save()
                todo_list.fields.add(field)
                todo_list.save()
                
        return redirect('todo_list_app:index')
        
    return render(request, 'todo_list/create_todo_list.html', {'new':True})


@login_required
def delete_todo_list(request, todo_list_id: int):
    """
    Delete todo list function. 
    
    Deletes todo list and redirects to index page.

    Requires todo_list_id as parameter.
    """
    if request.method == 'POST':
        todo_list = TodoList.objects.get(id=todo_list_id)
        if todo_list:
            if todo_list.owner == request.user:
                fields = todo_list.fields.all()
                fields.delete()
                todo_list.delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    return redirect('todo_list_app:index')


@login_required
def edit_todo_list(request,todo_list_id: int):
    """
    Edit todo list page view.
    
    If method is POST, edits todo list and redirects to index page. 
    
    If method is GET, returns edit todo list page.

    Requires todo_list_id as parameter.
    """
    if request.method == 'POST':
        print(request.POST)
        todo_list = TodoList.objects.get(id=todo_list_id)
        if todo_list:
            if todo_list.owner == request.user:
                todo_list.name = request.POST.get('name')
                new_fields = request.POST.getlist('fields_new')
                new_descriptions = request.POST.getlist('descriptions_new')
                new_deadlines = request.POST.getlist('deadlines_new')
                new_deadlines = [i if i != '' else None for i in new_deadlines]
                fields = [int(i) for i in request.POST.getlist('fields')]
                names = request.POST.getlist('names')
                descriptions = request.POST.getlist('descriptions')
                deadlines = request.POST.getlist('deadlines')  
                deadlines = [i if i != '' else None for i in deadlines]         
                todo_list.save()

                todo_list_fields = todo_list.fields.all()

                for i in todo_list_fields:
                    if i.id not in fields:
                        i.delete()
                print(fields)
                if fields:
                    for c,field in enumerate(fields):

                        field = TodoField.objects.get(id=field)
                        if field:
                            field.name = names[c]
                            field.text = descriptions[c]
                            field.deadline_at = deadlines[c]
                            field.save()

                if new_fields:
                    for c,i in enumerate(new_fields):
                        field = TodoField.objects.create(name=i, text=new_descriptions[c], checked=False, deadline_at=new_deadlines[c])
                        field.save()
                        todo_list.fields.add(field)
                        todo_list.save()

                return redirect('todo_list_app:index')
            

    else:
        todo_list = TodoList.objects.get(id=todo_list_id)
        if todo_list:
            if todo_list.owner == request.user:
                todo_fields = [
                    {
                        'id': i.id,
                        'name': i.name,
                        'text': i.text,
                        'checked': i.checked,
                        'deadline': datetime.date.strftime(i.deadline_at, '%Y-%m-%d')
                    }
                    if i.deadline_at is not None
                    else
                    {
                        'id': i.id,
                        'name': i.name,
                        'text': i.text,
                        'checked': i.checked,
                        'deadline': i.deadline_at
                    }
                    for i in todo_list.fields.all()
                ]

                return render(request, 'todo_list/create_todo_list.html', {'todo_list':todo_list, 'todo_fields':todo_fields})
            
    return redirect('todo_list_app:index')


@login_required
def list_of_todo_lists(request):
    """
    List of todo lists page view. 
    
    Returns list all of todo lists wich owner is the user that sent the request.
    """
    todo_lists = [
        {
            'id':i.id,
            'name':i.name,
            'owner':i.owner,
            'fields':[a for a in i.fields.all()]
        } 
        for i in TodoList.objects.filter(owner=request.user)
    ]     

    return render(request, 'todo_list/list_of_todo_lists.html', {'todo_lists':todo_lists})


@login_required
def check_task(request, todo_field_id: int):
    """
    Check task function.

    Checks task and returns success response.

    Requires todo_field_id as parameter.
    """
    field = TodoField.objects.get(id=todo_field_id)

    user_fields = []
    user_list = TodoList.objects.filter(owner=request.user)
    for i in user_list:
        for f in i.fields.all():
            user_fields.append(f)

        if field in user_fields:
            if field.checked == False:
                field.checked = True
            else:
                field.checked = False
            field.save()

            return JsonResponse({'response':'success'})
        

@login_required
def settings(request):
    """
    Settings page view.

    If method is POST, edits user options and redirects to settings page.

    If method is GET, returns settings page.
    """
    if request.method == 'POST':
        user_options = UserOptions.objects.get(user=request.user)
        user_options.theme = request.POST.get('theme')
        user_options.email_notifications = bool(int(request.POST.get('email_notifications')))
        
        user_options.dark_mode = bool(int(request.POST.get('theme')))
        user_options.save()

        if request.POST.get('username') != request.user.username:
            if User.objects.filter(username=request.POST.get('username')).exists():
                messages.add_message(request, messages.ERROR, 'This username already exists.')
                return redirect('todo_list_app:settings')
            else:
                user = User.objects.get(id=request.user.id)
                user.username = request.POST.get('username')
                user.save()
        
        if request.POST.get('email') != request.user.email:
            if User.objects.filter(email=request.POST.get('email')).exists():
                messages.add_message(request, messages.ERROR, 'Account with this email already exists.')
                return redirect('todo_list_app:settings')
            else:
                user = User.objects.get(id=request.user.id)
                user.email = request.POST.get('email')
                user.save()

        if request.POST.get('password') != '':
            if request.POST.get('password') == request.POST.get('password2'):
                user = User.objects.get(id=request.user.id)
                user.set_password(request.POST.get('password'))
                user.save()
            else:
                messages.add_message(request, messages.ERROR, 'Passwords do not match.')
                return redirect('todo_list_app:settings')
        
        return redirect('todo_list_app:settings')
    

    user = User.objects.get(id=request.user.id)
    user_options = UserOptions.objects.get(user=user)

    return render(request, 'todo_list/settings.html', {'user_options':user_options})


class ToDoAppPasswordResetView(PasswordResetView):
    """
    Django built-in PasswordResetView with custom template.
    """
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('todo_list_app:password_reset_done')

class ToDoAppPasswordResetDoneView(PasswordResetDoneView):
    """
    Django built-in PasswordResetDoneView with custom template.
    """
    template_name = 'registration/password_reset_done.html'

class ToDoAppPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Django built-in PasswordResetConfirmView with custom template.
    """
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('todo_list_app:password_reset_complete')

class ToDoAppPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Django built-in PasswordResetCompleteView with custom template.
    """
    template_name = 'registration/password_reset_complete.html'