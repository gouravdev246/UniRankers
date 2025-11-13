from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from leaderboard.models import Achievement
from .forms import ProfileForm


def signup_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number', '')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            user = User(
                name=name,
                phone_number=phone_number,
                email=email,
            )
            user.set_password(password) # Use set_password for hashing
            user.save()
            messages.success(request, "Account created!")
            return redirect('login')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('profile')  # Redirect to home or dashboard
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

@login_required
def profile_view(request):
    profile_user = request.user
    achievements = Achievement.objects.filter(user=profile_user).annotate(likes_count=Count('likes')).order_by('-created_at')
    total_points = achievements.aggregate(total=Coalesce(Sum('points'), 0))['total']
    skills = achievements.filter(category=Achievement.CATEGORY_SKILL)
    certificates = achievements.filter(category=Achievement.CATEGORY_CERTIFICATION)
    form = ProfileForm(instance=profile_user)
    return render(request, 'profile.html', {"profile_user": profile_user, "is_own_profile": True, "achievements": achievements, "total_points": total_points, "form": form, "skills": skills, "certificates": certificates})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Please fix the errors below.')
    return redirect('profile')


@login_required
def public_profile_view(request, user_id: int):
    try:
        profile_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('leaderboard')
    achievements = Achievement.objects.filter(user=profile_user).annotate(likes_count=Count('likes')).order_by('-created_at')
    total_points = achievements.aggregate(total=Coalesce(Sum('points'), 0))['total']
    skills = achievements.filter(category=Achievement.CATEGORY_SKILL)
    certificates = achievements.filter(category=Achievement.CATEGORY_CERTIFICATION)
    return render(request, 'profile.html', {"profile_user": profile_user, "is_own_profile": False, "achievements": achievements, "total_points": total_points, "skills": skills, "certificates": certificates})
