from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import taskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):

    return render(request,'index.html')



def signup(request):

    if request.method == 'GET':
        return render(request,'signup.html', {
            'form' : UserCreationForm
        })

    else: 
        if request.POST['password1'] == request.POST['password2']:
            # Register user
            try:
                # Create user
                user = User.objects.create_user(username=request.POST['username'], 
                password=request.POST['password1']) 

                # Save in Database
                user.save() 
                login(request,user) # Cookies
                return redirect('tasks') # Redirect to views tasks
            
            except IntegrityError:
                return render(request,'signup.html', {
                    'form' : UserCreationForm,
                    'error' : 'Username already exists'
                })
        # Return message
        return render(request,'signup.html', {
            'form' : UserCreationForm,
            'error' : 'Password do not match'
        })
    
# List tasks
@login_required
def tasks (request):



    # Filter to get the current user task
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True) 

    return render(request, 'tasks.html', {
        'tasks' : tasks
    })

# List task completed
def tasks_completed (request):

    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed') 

    return render(request, 'tasks.html', {
        'tasks' : tasks
    })

# Create
@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_tasks.html',{
            # Import custom form
            'form' : taskForm 
        })
    else:
        try:
            form = taskForm(request.POST)

            new_task = form.save(commit=False) 
            # Relate task to user
            new_task.user = request.user 
            # Save task
            new_task.save() 

            return redirect('tasks') 
        except ValueError:
            return render(request, 'create_tasks.html',{
                'form' : taskForm,
                'error' : 'Please provide valide data'
            })

# Show task
@login_required
def task_details(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = taskForm (instance=task)
        return render(request, 'task_details.html', {
            'task' : task,
            'form' : form

        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = taskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_details.html', {
                'task' : task,
                'form' : form,
                'error' : "Error updating task"
            })

# Complete / Update
@login_required
def task_complete(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

# Delete
@login_required
def task_delete(request, task_id):

    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    

# Logout
def signout(request):
    logout(request)
    return redirect('index')

# Login
def signin(request):

    if request.method == 'GET':
        return render(request, 'login.html',{
            'form' : AuthenticationForm
            
        })
    else:

        user = authenticate(
            request, username=request.POST['username'], 
            password=request.POST['password'])

        if user is None:
            return render(request, 'login.html',{
            'form' : AuthenticationForm,
            'error' : 'Username or Password is incorrect'

            })
        else:
            login(request,user)
            return redirect('tasks')
