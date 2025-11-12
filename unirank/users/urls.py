from django.contrib import admin
from django.urls import path, include
from . import views
from .views import login_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    # path('auth/', include('social_django.urls', namespace='social')),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

]