from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import User
from .forms import AchievementForm
from .models import Achievement


def leaderboard_view(request):
    users_qs = (
        User.objects
        .annotate(total_points=Coalesce(Sum("achievements__points"), 0))
        .order_by("-total_points", "name")
    )

    paginator = Paginator(users_qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Simple rank calculation across current page
    start_rank = (page_obj.number - 1) * paginator.per_page
    ranked_users = [
        {"rank": start_rank + idx + 1, "user": u, "total_points": u.total_points}
        for idx, u in enumerate(page_obj.object_list)
    ]

    context = {
        "page_obj": page_obj,
        "ranked_users": ranked_users,
        "total_count": paginator.count,
    }
    return render(request, "leaderboard.html", context)


def _compute_points(category: str, cgpa: float | None) -> int:
    if category == Achievement.CATEGORY_CERTIFICATION:
        return 10
    if category == Achievement.CATEGORY_SKILL:
        return 5
    if category == Achievement.CATEGORY_BADGE:
        return 3
    if category == Achievement.CATEGORY_CGPA:
        try:
            return int(round((cgpa or 0) * 10))
        except Exception:
            return 0
    return 1


@login_required
def add_achievement_view(request):
    if request.method == "POST":
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            ach = form.save(commit=False)
            ach.user = request.user
            ach.points = _compute_points(ach.category, ach.cgpa)
            ach.save()
            messages.success(request, "Achievement added. Points awarded: %d" % ach.points)
            return redirect("leaderboard")
        messages.error(request, "Please correct the errors below.")
    else:
        form = AchievementForm()
    return render(request, "add_achievement.html", {"form": form})
