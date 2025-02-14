from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponse
from django.contrib import messages
from .models import TodoList, TodoField, UserOptions
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView 
from django.db.models import Q
import re

# Create your views here.

def index(request):
    """
    View function for home page of site. 
    
    If user is authenticated, returns list of todo lists.

    If user isnt authenticated redirects to login page.
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            todo_lists = [
                {
                    'id':i.id,
                    'name':i.name,
                    'created_by':i.created_by,
                    'owner':[a for a in i.owner.all()],
                    'fields':[a for a in i.fields.all()],
                    'hash':i.hash,
                    'access_granted':i.access_granted,
                }
                for i in TodoList.objects.filter(owner=request.user).order_by('-created_at')
            ]     

            return render(request, 'todo_list/index.html', {'todo_lists':todo_lists})
        
        else:
            return redirect('todo_list_app:login')
    else:
        # return status code 405 if method is not GET
        return HttpResponse(status=405)

def list_details(request, todo_list_hash: str):
        """
        View function for todo list details page.
        
        Returns todo list details.
        
        Todo list hash is used to get todo list and is required parameter.
        """
        if request.method == 'GET':
            todo_lists = [
                {
                    'id':i.id,
                    'name':i.name,
                    'created_by':i.created_by,
                    'owner':[a for a in i.owner.all()],
                    'fields':[a for a in i.fields.all()],
                    'hash':i.hash,
                    'access_granted':i.access_granted,
                } 
                for i in TodoList.objects.filter(hash=todo_list_hash)
            ]
            
            return render(request, 'todo_list/detail.html', {'todo_lists':todo_lists})
        else:
            # return status code 405 if method is not GET
            return HttpResponse(status=405)



def user_login(request):
    """
    View function for login page.

    If user is authenticated, redirects to index page.

    If user is not authenticated, returns login page.
    """
    if request.method =='POST':
        if request.user.is_authenticated == False:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect('todo_list_app:index')
            else:
                messages.add_message(request, messages.ERROR, 'You`ve entered a wrong username or password.')

                return redirect('todo_list_app:login')
        
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('todo_list_app:index')
        else:
            return render(request, 'todo_list/login.html')
    
    return HttpResponse(status=405)


def signup(request):
    """
    View function for signup page.

    If user is authenticated, redirects to index page.

    If user is not authenticated, returns signup page.
    """
    if request.method == 'POST':
        if request.user.is_authenticated == False:
            email = request.POST.get('email')
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
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
                    # validate email
                    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None:
                        # validate username
                        if re.match(r'^[a-zA-Z0-9_]+$', username) is not None:
                            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                            user.save()
                            user_options = UserOptions.objects.create(user=user)
                            user_options.dark_mode = False
                            user_options.save()

                            return redirect('todo_list_app:login')
                        else:
                            messages.add_message(request, messages.ERROR, 'Invalid username. Username can only contain letters, numbers and underscores.')

                            return redirect('todo_list_app:signup')
                    
                    else:
                        messages.add_message(request, messages.ERROR, 'Invalid email.')

                        return redirect('todo_list_app:signup')
                    
            else:
                messages.add_message(request, messages.ERROR, 'Passwords do not match.')

                return redirect('todo_list_app:signup')
            
        else:
            return HttpResponse(status=405)
        
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('todo_list_app:index')
        else:
            return render(request, 'todo_list/signup.html')
    
    return HttpResponse(status=405)


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
        name = request.POST.get('name')
        new_fields = request.POST.getlist('fields_new')
        new_descriptions = request.POST.getlist('descriptions_new')
        new_deadlines = request.POST.getlist('deadlines_new')
        shared = request.POST.get('is-shared')
        new_deadlines = [i if i != '' else None for i in new_deadlines]
        todo_list = TodoList.objects.create(name=name, created_by=request.user, access_granted=bool(int(shared)))
        todo_list.owner.add(request.user)
        todo_list.hash = todo_list._create_hash()
        todo_list.save()
        if new_fields:
            for c,i in enumerate(new_fields):
                field = TodoField.objects.create(name=i, text=new_descriptions[c], checked=False, deadline_at=new_deadlines[c])
                field.save()
                todo_list.fields.add(field)
                todo_list.save()
                
        return redirect('todo_list_app:index')
    
    elif request.method == 'GET':
        return render(request, 'todo_list/create_todo_list.html', {'new':True})
    
    else:
        return HttpResponse(status=405)


@login_required
def delete_todo_list(request, todo_list_hash: str):
    """
    Delete todo list function. 
    
    Deletes todo list and redirects to index page.

    Requires todo_list_id as parameter.
    """
    if request.method == 'POST':
        todo_list = get_object_or_404(TodoList,hash=todo_list_hash)
        if request.user == todo_list.created_by:
            fields = todo_list.fields.all()
            fields.delete()
            todo_list.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        elif request.user in todo_list.owner.all():
            todo_list.owner.remove(request.user)
            todo_list.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        return redirect('todo_list_app:index')
    
    else:
        return HttpResponse(status=405)


@login_required
def edit_todo_list(request,todo_list_hash: str):
    """
    Edit todo list page view.
    
    If method is POST, edits todo list and redirects to index page. 
    
    If method is GET, returns edit todo list page.

    Requires todo_list_id as parameter.
    """
    if request.method == 'POST':
        todo_list = get_object_or_404(TodoList,hash=todo_list_hash)
        if request.user in todo_list.owner.all():
            todo_list.name = request.POST.get('name')
            todo_list.access_granted = bool(int(request.POST.get('is-shared')))
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

    elif request.method == 'GET':
        todo_list = get_object_or_404(TodoList,hash=todo_list_hash)
        if request.user in todo_list.owner.all():
            todo_fields = [
                {
                    'id': i.id,
                    'name': i.name,
                    'text': i.text,
                    'checked': i.checked,
                    'deadline_at': datetime.date.strftime(i.deadline_at, '%Y-%m-%d')
                }
                if i.deadline_at is not None
                else
                {
                    'id': i.id,
                    'name': i.name,
                    'text': i.text,
                    'checked': i.checked,
                    'deadline_at': i.deadline_at
                }
                for i in todo_list.fields.all()
            ]

            return render(request, 'todo_list/create_todo_list.html', {'todo_list':todo_list, 'todo_fields':todo_fields})
    else:
        return HttpResponse(status=405)


@login_required
def list_of_todo_lists(request):
    """
    List of todo lists page view. 
    
    Returns list all of todo lists wich owner is the user that sent the request.
    """
    if request.method == 'GET':
        todo_lists = [
            {
                'id':i.id,
                'name':i.name,
                'created_by':i.created_by,
                'owner':[a for a in i.owner.all()],
                'fields':[a for a in i.fields.all()],
                'hash':i.hash,
            } 
            for i in TodoList.objects.filter(owner=request.user)
        ]     

        return render(request, 'todo_list/list_of_todo_lists.html', {'todo_lists':todo_lists})

    else:
        return HttpResponse(status=405)


@login_required
def check_task(request, todo_field_id: int):
    """
    Check task function.

    Checks task and returns success response.

    Requires todo_field_id as parameter.
    """
    if request.method == 'POST':
        field = get_object_or_404(TodoField,id=todo_field_id)

        user_fields = []
        user_list = TodoList.objects.filter(Q(created_by=request.user)|Q(access_granted=True))

        for i in user_list:
            for f in i.fields.all():
                user_fields.append(f)

            if field in user_fields:
                if field.checked == False:
                    field.checked = True
                else:
                    field.checked = False
                field.save()

                return HttpResponse('success')
        
        return HttpResponse(status=403)

    else:
        return HttpResponse(status=405)
        
@login_required
def add_to_my_list(request, todo_list_hash: str):
    """
    Add to my list function.

    Adds todo list to user's list and returns success response.

    Requires todo_list_id as parameter.
    """
    if request.method == 'POST':
        todo_list = get_object_or_404(TodoList, hash=todo_list_hash)
        if request.user not in todo_list.owner.all():
            todo_list.owner.add(request.user)
            todo_list.save()
        return HttpResponse('reload', status=200)
            
    else:
        return HttpResponse(status=405)

@login_required
def remove_from_shared_list(request, todo_list_id: int, user_id: int):
    """
    Remove from shared list function.

    Removes user from todo list and returns success response.

    Requires todo_list_id and user_id as parameters.
    """
    if request.method == 'POST':
        todo_list = get_object_or_404(TodoList,id=todo_list_id)
        user = get_object_or_404(User, id=user_id)
        if request.user == todo_list.created_by:
            if user != request.user:
                todo_list.owner.remove(user_id)
                todo_list.save()
        return HttpResponse('reload')
            
    else:
        return HttpResponse(status=405)

@login_required
def settings(request):
    """
    Settings page view.

    If method is POST, edits user options and redirects to settings page.

    If method is GET, returns settings page.
    """
    if request.method == 'POST':
        user_options = UserOptions.objects.get(user=request.user)
        user_options.mode = request.POST.get('theme')
        user_options.font_style = request.POST.get('font_style')
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
        
        if request.POST.get('first_name') != request.user.first_name or request.POST.get('last_name') != request.user.last_name:
            user = User.objects.get(id=request.user.id)
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            user.first_name = first_name
            user.last_name = last_name
            user.save()

        return redirect('todo_list_app:settings')
    

    user = User.objects.get(id=request.user.id)
    user_options = UserOptions.objects.get(user=user)

    # print()
    # print(user_options.font_style)
    return render(request, 'todo_list/settings.html', {'user_options':user_options, 'font_styles':UserOptions.font_style_choices, 'modes': UserOptions.mode_choices})

@login_required
def account_delete(request):
    """
    Delete account function.

    Deletes user account and redirects to login page.
    """
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.delete()
        return redirect('todo_list_app:login')
    
    else:
        return HttpResponse(status=405)

def accept_cookies(request):
    """
    Accept cookies function.

    Sets cookie_message to 0 and returns success response.
    """
    if request.method == 'POST':
        request.session['cookie_message'] = 0
        return HttpResponse('success')
    else:
        return HttpResponse(status=405)
    
    
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