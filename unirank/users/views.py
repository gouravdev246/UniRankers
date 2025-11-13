from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import Coalesce
from leaderboard.models import Achievement


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
    achievements = Achievement.objects.filter(user=request.user).order_by('-created_at')
    total_points = achievements.aggregate(total=Coalesce(Sum('points'), 0))['total']
    return render(request, 'profile.html', {"achievements": achievements, "total_points": total_points})
