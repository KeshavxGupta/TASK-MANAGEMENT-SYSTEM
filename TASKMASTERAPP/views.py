from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from datetime import timedelta
from .forms import CustomUserCreationForm, TaskForm
from .models import Task, Feedback, CustomUser

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'user'  # Set default user type
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Account created successfully! Please login to continue.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'admin':
            return redirect('admin_dashboard')
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'user')  # Default to 'user' if not specified
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if the user type matches
            if user.user_type != user_type:
                messages.error(request, f'Invalid user type. Please select {user.get_user_type_display()}.')
                return render(request, 'users/login.html')
                
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            if user.user_type == 'admin':
                return redirect('admin_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('index')

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    
    for task in tasks:
        task.update_status()
        task.save()

    filter_param = request.GET.get('filter', 'all')
    if filter_param == 'pending':
        tasks = tasks.filter(status='pending')
    elif filter_param == 'completed':
        tasks = tasks.filter(status='completed')
    elif filter_param == 'overdue':
        tasks = tasks.filter(status='overdue')

    context = {
        'user': request.user,
        'tasks': tasks,
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(status='completed').count(),
        'pending_tasks': tasks.filter(status='pending').count(),
        'overdue_tasks': tasks.filter(status='overdue').count(),
    }

    return render(request, 'users/dashboard.html', context)

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        # Handle profile picture upload first
        if 'profile_picture' in request.FILES:
            # Delete the old profile picture if it exists and is not the default
            if user.profile_picture and 'default-profile.jpg' not in user.profile_picture.name:
                user.profile_picture.delete(save=False)
            user.profile_picture = request.FILES['profile_picture']

        # Update other user fields
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone', user.phone_number)
        user.gender = request.POST.get('gender', user.gender)
        user.date_of_birth = request.POST.get('dob', user.date_of_birth)
        user.address = request.POST.get('address', user.address)
        user.bio = request.POST.get('bio', user.bio)
        user.social = request.POST.get('social', user.social)

        # Handle password change if provided
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
            user.save()
            login(request, user)  # Re-login the user
            messages.success(request, "Profile updated and re-authenticated due to password change.")
        else:
            user.save()
            messages.success(request, "Profile updated successfully.")

        return redirect('dashboard')

    return render(request, 'users/profile.html', {'user': user})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('dashboard')

@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.status = 'pending' if task.status == 'completed' else 'completed'
    task.save()
    return redirect('dashboard')

@login_required
def calendar_view(request):
    return render(request, 'calendar.html')

@login_required
@require_GET
def calendar_events(request):
    tasks = Task.objects.filter(user=request.user)
    events = []

    for task in tasks:
        events.append({
            'id': task.id,
            'title': task.title,
            'start': task.due_date.isoformat() if task.due_date else None,
            'priority': task.priority,
            'status': task.status,
            'description': task.description,
            'category': task.category,
            'tags': task.tags,
            'url': f'/edit-task/{task.id}/',
            'backgroundColor': {
                'high': '#fecaca',
                'medium': '#fef08a',
                'low': '#bbf7d0',
                'undone': '#fca5a5',
            }.get(task.status, '#e5e7eb'),
            'borderColor': {
                'high': '#ef4444',
                'medium': '#eab308',
                'low': '#22c55e',
                'undone': '#dc2626',
            }.get(task.status, '#9ca3af'),
            'textColor': '#1f2937',
            'extendedProps': {
                'priority': task.priority,
                'status': task.status,
                'description': task.description,
                'category': task.category,
                'tags': task.tags
            }
        })
    return JsonResponse(events, safe=False)

def feedback_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            Feedback.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, 'Thank you for your feedback!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fill in all fields before submitting.')

    return render(request, 'feedback.html')

def about(request):
    return render(request, 'about.html')

def demo(request):
    return render(request, 'demo.html')

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    return render(request, 'task_detail.html', {'task': task})

@login_required
def admin_feedback_view(request):
    if not request.user.is_admin():
        return redirect('index')

    feedbacks = Feedback.objects.all()
    return render(request, 'admin/feedback.html', {'feedbacks': feedbacks})

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    # Get counts for dashboard cards
    total_users = CustomUser.objects.count()
    total_tasks = Task.objects.count()
    
    # Get today's counts
    today = timezone.now().date()
    new_users_today = CustomUser.objects.filter(date_joined__date=today).count()
    new_tasks_today = Task.objects.filter(created_at__date=today).count()
    
    # Get active users in last 24 hours
    last_24_hours = timezone.now() - timedelta(hours=24)
    active_users = CustomUser.objects.filter(last_login__gte=last_24_hours).count()
    
    # Get unread feedback count
    new_feedback = Feedback.objects.filter(is_read=False).count()
    
    # Get recent users and tasks
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    recent_tasks = Task.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_tasks': total_tasks,
        'new_users_today': new_users_today,
        'new_tasks_today': new_tasks_today,
        'active_users': active_users,
        'new_feedback': new_feedback,
        'recent_users': recent_users,
        'recent_tasks': recent_tasks,
    }
    
    return render(request, 'admin/dashboard.html', context)

@user_passes_test(is_admin, login_url='login')
def admin_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'admin/users.html', {'users': users})

@user_passes_test(is_admin, login_url='login')
def admin_tasks(request):
    tasks = Task.objects.all().order_by('-created_at')
    
    # Apply filters if provided
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    category_filter = request.GET.get('category')
    
    if status_filter and status_filter != 'all':
        tasks = tasks.filter(status=status_filter)
    
    if priority_filter and priority_filter != 'all':
        tasks = tasks.filter(priority=priority_filter)
    
    if category_filter and category_filter != 'all':
        tasks = tasks.filter(category=category_filter)
    
    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'category_filter': category_filter,
    }
    
    return render(request, 'admin/tasks.html', context)

@user_passes_test(is_admin, login_url='login')
def admin_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    # Mark all feedback as read
    Feedback.objects.filter(is_read=False).update(is_read=True)
    return render(request, 'admin/feedback.html', {'feedbacks': feedbacks})

@user_passes_test(is_admin, login_url='login')
def admin_settings(request):
    if request.method == 'POST':
        # Handle settings update
        # Add your settings logic here
        messages.success(request, 'Settings updated successfully!')
        return redirect('admin_settings')
    return render(request, 'admin/settings.html')

@user_passes_test(is_admin, login_url='login')
def toggle_user_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"User {user.username}'s status has been updated.")
    return redirect('admin_users')

@user_passes_test(is_admin, login_url='login')
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    username = user.username
    user.delete()
    messages.success(request, f"User {username} has been deleted.")
    return redirect('admin_users')

