from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Count, Q
from .forms import NationalIDLoginForm
from .models import User
from exams.models import UserExam


@csrf_protect
@never_cache
def login_view(request):
    """Handle user login with National ID"""
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    
    if request.method == 'POST':
        form = NationalIDLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.name}!')
            
            # Redirect to next page or dashboard
            next_page = request.GET.get('next', 'authentication:dashboard')
            return redirect(next_page)
        else:
            messages.error(request, 'Login failed. Please check your National ID.')
    else:
        form = NationalIDLoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})


@login_required
def logout_view(request):
    """Handle user logout"""
    user_name = request.user.name
    logout(request)
    messages.info(request, f'Goodbye, {user_name}! You have been logged out.')
    return redirect('authentication:login')


@login_required
def dashboard_view(request):
    """Display user dashboard with assigned exams"""
    # Admin users should not see any exams
    if request.user.is_admin:
        context = {
            'assigned_exams': [],
            'completed_exams': [],
            'pending_exams': [],
        }
        return render(request, 'authentication/dashboard.html', context)
    
    user_exams = UserExam.objects.filter(user=request.user).select_related('exam', 'exam__course').prefetch_related('exam_sessions')
    
    # Categorize exams by status based on exam sessions
    assigned_exams = user_exams
    completed_exams = []
    pending_exams = []
    
    for user_exam in user_exams:
        # Check if user has any submitted sessions for this exam
        submitted_sessions = user_exam.exam_sessions.filter(is_submitted=True)
        if submitted_sessions.exists():
            completed_exams.append(user_exam)
        else:
            pending_exams.append(user_exam)
    
    context = {
        'assigned_exams': assigned_exams,
        'completed_exams': completed_exams,
        'pending_exams': pending_exams,
    }
    
    return render(request, 'authentication/dashboard.html', context)


@login_required
def profile_view(request):
    """Display user profile information"""
    user_exams = UserExam.objects.filter(user=request.user)
    
    # Calculate statistics
    total_assigned = user_exams.count()
    total_completed = user_exams.filter(exam_sessions__is_submitted=True).distinct().count()
    total_pending = total_assigned - total_completed
    
    # Calculate average score for completed exams
    # Note: Score calculation would need to be implemented and stored
    # For now, setting average_score to 0 until score storage is implemented
    average_score = 0
    
    context = {
        'total_assigned': total_assigned,
        'total_completed': total_completed,
        'total_pending': total_pending,
        'average_score': average_score,
    }
    
    return render(request, 'authentication/profile.html', context)


def check_session(request):
    """AJAX endpoint to check if user session is still valid"""
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'user_id': request.user.id,
            'name': request.user.name
        })
    else:
        return JsonResponse({'authenticated': False})
