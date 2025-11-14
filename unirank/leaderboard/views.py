from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
import json
from django.http import HttpResponseForbidden

from users.models import CustomUser as User
from .forms import AchievementForm, SkillsForm
from .models import Achievement, Like, Comment


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


@login_required
def like_toggle(request, achievement_id):
    if request.method != "POST":
        return HttpResponseBadRequest()
    try:
        achievement = Achievement.objects.get(pk=achievement_id)
    except Achievement.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    like, created = Like.objects.get_or_create(user=request.user, achievement=achievement)
    if not created:
        like.delete()
    count = achievement.likes.count()
    return JsonResponse({"liked": created, "count": count})


@login_required
@login_required
def comment_create(request, achievement_id):
    if request.method != "POST":
        return HttpResponseBadRequest()
    content = request.POST.get("content")
    parent_id = request.POST.get("parent")
    if content is None:
        try:
            data = json.loads(request.body.decode("utf-8"))
            content = (data.get("content") or "").strip()
            parent_id = data.get("parent")
        except Exception:
            content = ""
            parent_id = None
    else:
        content = content.strip()
    if len(content) > 300:
        return JsonResponse({"error": "Too long"}, status=400)
    if not content:
        return JsonResponse({"error": "Empty"}, status=400)
    try:
        achievement = Achievement.objects.get(pk=achievement_id)
    except Achievement.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    parent = None
    if parent_id:
        try:
            parent = Comment.objects.get(pk=parent_id, achievement=achievement)
        except Comment.DoesNotExist:
            parent = None
    c = Comment.objects.create(user=request.user, achievement=achievement, parent=parent, content=content)
    return JsonResponse({
        "id": c.id,
        "user": c.user.name,
        "avatar": getattr(c.user.profile_photo, "url", ""),
        "content": c.content,
        "created_at": c.created_at.isoformat(),
        "parent": c.parent_id,
    })


def comments_list(request, achievement_id):
    try:
        achievement = Achievement.objects.get(pk=achievement_id)
    except Achievement.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    page = int(request.GET.get("page", 1))
    qs = Comment.objects.filter(achievement=achievement, parent__isnull=True).order_by("-created_at")
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page)
    items = []
    for c in page_obj.object_list:
        items.append({
            "id": c.id,
            "user": c.user.name,
            "avatar": getattr(c.user.profile_photo, "url", ""),
            "content": c.content,
            "created_at": c.created_at.isoformat(),
            "replies": [
                {
                    "id": r.id,
                    "user": r.user.name,
                    "avatar": getattr(r.user.profile_photo, "url", ""),
                    "content": r.content,
                    "created_at": r.created_at.isoformat(),
                }
                for r in c.replies.all().order_by("created_at")
            ],
        })
    return JsonResponse({
        "items": items,
        "page": page_obj.number,
        "has_next": page_obj.has_next(),
    })


@login_required
def manage_skills_view(request):
    skills = Achievement.objects.filter(user=request.user, category=Achievement.CATEGORY_SKILL).order_by("-created_at")
    if request.method == "POST":
        form = SkillsForm(request.POST)
        if form.is_valid():
            ach = form.save(commit=False)
            ach.title = form.cleaned_data.get("value")
            ach.user = request.user
            ach.category = Achievement.CATEGORY_SKILL
            ach.points = 5
            ach.save()
            messages.success(request, "Skill added.")
            return redirect("manage_skills")
        messages.error(request, "Please correct the errors below.")
    else:
        form = SkillsForm()
    return render(request, "manage_skills.html", {"skills": skills, "form": form})


@login_required
def achievement_delete_view(request, achievement_id):
    if request.method != "POST":
        return HttpResponseBadRequest()
    try:
        achievement = Achievement.objects.get(pk=achievement_id)
    except Achievement.DoesNotExist:
        messages.error(request, "Achievement not found.")
        return redirect("profile")
    if achievement.user_id != request.user.id:
        return HttpResponseForbidden()
    achievement.delete()
    messages.success(request, "Achievement deleted.")
    return redirect("profile")
