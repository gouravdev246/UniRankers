from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required


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
            return redirect('home')  # Redirect to home or dashboard
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, 'login.html')




# def login_view(request):
#     return render(request, 'login1.html')

@login_required
def home(request):
    return render(request, 'home.html')