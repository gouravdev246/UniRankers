from django.urls import path
from . import views

urlpatterns = [
    path("", views.leaderboard_view, name="leaderboard"),
    path("add/", views.add_achievement_view, name="add_achievement"),
    path("<int:achievement_id>/like/", views.like_toggle, name="like_toggle"),
    path("<int:achievement_id>/comments/", views.comments_list, name="comments_list"),
    path("<int:achievement_id>/comment/", views.comment_create, name="comment_create"),
    path("skills/", views.manage_skills_view, name="manage_skills"),
]
