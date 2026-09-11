from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import User
from courses.models import Enrollment, Progress
from quizzes.models import Quiz, Result

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to LearnTrack!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('landing')

@login_required
def dashboard(request):
    user = request.user
    
    enrollments = Enrollment.objects.filter(user=user)
    total_courses = enrollments.count()
    
    # Calculate completed courses
    completed_courses = 0
    pending_courses = 0
    for enrollment in enrollments:
        total_lessons = enrollment.course.lessons.count()
        completed_lessons = Progress.objects.filter(user=user, lesson__course=enrollment.course, completed=True).count()
        if total_lessons > 0 and completed_lessons == total_lessons:
            completed_courses += 1
        else:
            pending_courses += 1
            
    recent_results = Result.objects.filter(user=user).select_related('quiz__course').order_by('-timestamp')[:5]
    
    average_score = 0
    total_results = Result.objects.filter(user=user)
    if total_results.exists():
        average_score = sum([r.score for r in total_results]) / total_results.count()
        
    context = {
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'pending_courses': pending_courses,
        'recent_results': recent_results,
        'average_score': round(average_score, 1),
    }
    return render(request, 'dashboard.html', context)
