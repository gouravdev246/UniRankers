from django.urls import path
from . import views

urlpatterns = [
    path("", views.leaderboard_view, name="leaderboard"),
    path("add/", views.add_achievement_view, name="add_achievement"),
]
