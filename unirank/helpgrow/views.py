from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import HelpRequest, RequestAcceptance, Bookmark, Report, Team, TeamMembership, ChatMessage, Notification
from .forms import HelpRequestForm, RequestCommentForm


@login_required
@ensure_csrf_cookie
def helpgrow_page(request):
    form = HelpRequestForm()
    qs = HelpRequest.objects.all()
    req_type = request.GET.get("type")
    urgency = request.GET.get("urgency")
    order = request.GET.get("order")
    if req_type:
        qs = qs.filter(request_type=req_type)
    if urgency:
        qs = qs.filter(urgency=urgency)
    if order == "date":
        qs = qs.order_by("-created_at")
    elif order == "urgency":
        qs = qs.order_by("-urgency")
    requests = qs.select_related("author").prefetch_related("acceptances", "comments", "team__memberships")
    return render(request, "helpgrow.html", {"form": form, "requests": requests})


@login_required
def request_create(request):
    if request.method != "POST":
        return HttpResponseBadRequest()
    one_hour_ago = timezone.now() - timezone.timedelta(hours=1)
    if HelpRequest.objects.filter(author=request.user, created_at__gte=one_hour_ago).count() >= 5:
        messages.error(request, "Rate limit exceeded.")
        return redirect("helpgrow")
    form = HelpRequestForm(request.POST)
    if form.is_valid():
        r = form.save(commit=False)
        r.author = request.user
        r.save()
        messages.success(request, "Request created.")
        return redirect("helpgrow")
    messages.error(request, "Please correct the errors.")
    return redirect("helpgrow")


@login_required
def accept_request(request, request_id):
    if request.method != "POST":
        return HttpResponseBadRequest()
    try:
        req = HelpRequest.objects.get(pk=request_id)
    except HelpRequest.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    acc, created = RequestAcceptance.objects.get_or_create(request=req, user=request.user)
    if created:
        Notification.objects.create(user=req.author, message="Your request was accepted")
        if req.request_type in (HelpRequest.TYPE_HACKATHON, HelpRequest.TYPE_TEAM):
            team, _ = Team.objects.get_or_create(request=req)
            TeamMembership.objects.get_or_create(team=team, user=request.user)
            TeamMembership.objects.get_or_create(team=team, user=req.author, approved=True)
    return JsonResponse({"accepted": True})


@login_required
def comment_request(request, request_id):
    if request.method != "POST":
        return HttpResponseBadRequest()
    try:
        req = HelpRequest.objects.get(pk=request_id)
    except HelpRequest.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    form = RequestCommentForm(request.POST)
    if form.is_valid():
        c = form.save(commit=False)
        c.request = req
        c.user = request.user
        c.save()
        Notification.objects.create(user=req.author, message="New comment on your request")
        return JsonResponse({"id": c.id, "user": getattr(c.user, "name", ""), "content": c.content, "created_at": c.created_at.isoformat()})
    return JsonResponse({"errors": form.errors}, status=400)


@login_required
def bookmark_toggle(request, request_id):
    if request.method != "POST":
        return HttpResponseBadRequest()
    try:
        req = HelpRequest.objects.get(pk=request_id)
    except HelpRequest.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    b, created = Bookmark.objects.get_or_create(request=req, user=request.user)
    if not created:
        b.delete()
    return JsonResponse({"bookmarked": created})


@login_required
def report_create(request, request_id):
    if request.method != "POST":
        return HttpResponseBadRequest()
    reason = (request.POST.get("reason") or "").strip()
    if not reason:
        return JsonResponse({"error": "Empty"}, status=400)
    try:
        req = HelpRequest.objects.get(pk=request_id)
    except HelpRequest.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    Report.objects.create(request=req, user=request.user, reason=reason)
    return JsonResponse({"reported": True})


@login_required
def request_delete(request, request_id):
    if request.method != "POST":
        return HttpResponseBadRequest()
    try:
        req = HelpRequest.objects.get(pk=request_id)
    except HelpRequest.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    if req.author_id != request.user.id:
        return JsonResponse({"error": "Forbidden"}, status=403)
    req.delete()
    return JsonResponse({"deleted": True})


@login_required
def team_approve(request, request_id, user_id):
    if request.method != "POST":
        return HttpResponseBadRequest()
    try:
        req = HelpRequest.objects.get(pk=request_id, author=request.user)
    except HelpRequest.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    try:
        team = req.team
    except Team.DoesNotExist:
        return JsonResponse({"error": "No team"}, status=404)
    try:
        m = TeamMembership.objects.get(team=team, user_id=user_id)
    except TeamMembership.DoesNotExist:
        return JsonResponse({"error": "No member"}, status=404)
    m.approved = True
    m.save()
    Notification.objects.create(user=m.user, message="Approved for team")
    return JsonResponse({"approved": True})


@login_required
def chat_post(request, request_id):
    if request.method != "POST":
        return HttpResponseBadRequest()
    try:
        team = Team.objects.get(request_id=request_id)
    except Team.DoesNotExist:
        return JsonResponse({"error": "No team"}, status=404)
    content = (request.POST.get("content") or "").strip()
    if not content:
        return JsonResponse({"error": "Empty"}, status=400)
    ChatMessage.objects.create(team=team, sender=request.user, content=content)
    return JsonResponse({"posted": True})
