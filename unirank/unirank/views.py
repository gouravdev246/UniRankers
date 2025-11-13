from django.shortcuts import render
from django.contrib import messages
from users.models import ContactMessage
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not subject or not message:
            messages.error(request, 'All fields are required.')
        else:
            ContactMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            messages.success(request, 'Thanks! Your message has been sent.')
    return render(request, 'contact.html')
# def login(request):
#     return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
