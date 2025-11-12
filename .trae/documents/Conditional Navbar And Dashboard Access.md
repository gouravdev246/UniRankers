## Goal
Update the navbar to hide Login/Sign Up when the user is authenticated and show Logout (and Dashboard). Add a protected Dashboard page accessible only after login.

## Changes
1. Navbar logic in `templates/base.html`:
   - Wrap auth buttons with `{% if user.is_authenticated %}`.
   - Show Logout when authenticated; show Login/Sign Up otherwise.
   - Update Dashboard link to `{% url 'dashboard' %}` and render it only for authenticated users.
2. Dashboard route:
   - Add `dashboard` view in `unirank/unirank/views.py` with `@login_required`.
   - Register `path('dashboard/', views.dashboard, name='dashboard')` in `unirank/unirank/urls.py`.
   - Create `templates/dashboard.html` using the orange/white theme and Bootstrap.

## Validation
- Logged-out users: Dashboard redirects to login; navbar shows Login/Sign Up only.
- Logged-in users: Navbar shows Logout (not Login/Sign Up); Dashboard link is visible and loads the page.

Confirm and I’ll implement the changes immediately.