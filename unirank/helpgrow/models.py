from django.db import models
from django.conf import settings


class HelpRequest(models.Model):
    TYPE_TEAM = "TEAM"
    TYPE_GUIDANCE = "GUIDANCE"
    TYPE_HACKATHON = "HACKATHON"
    TYPE_OTHER = "OTHER"
    TYPE_CHOICES = (
        (TYPE_TEAM, "Team Formation"),
        (TYPE_GUIDANCE, "Guidance Needed"),
        (TYPE_HACKATHON, "Hackathon Partner"),
        (TYPE_OTHER, "Other"),
    )
    URGENCY_LOW = "LOW"
    URGENCY_MEDIUM = "MEDIUM"
    URGENCY_HIGH = "HIGH"
    URGENCY_CHOICES = (
        (URGENCY_LOW, "Low"),
        (URGENCY_MEDIUM, "Medium"),
        (URGENCY_HIGH, "High"),
    )
    STATUS_OPEN = "OPEN"
    STATUS_CLOSED = "CLOSED"
    STATUS_CHOICES = (
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSED, "Closed"),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="help_requests")
    title = models.CharField(max_length=200)
    request_type = models.CharField(max_length=16, choices=TYPE_CHOICES)
    description = models.TextField()
    required_skills = models.CharField(max_length=255, blank=True)
    urgency = models.CharField(max_length=16, choices=URGENCY_CHOICES)
    tags = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class RequestComment(models.Model):
    request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="help_comments")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class RequestAcceptance(models.Model):
    request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE, related_name="acceptances")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="help_acceptances")
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ("request", "user")


class Bookmark(models.Model):
    request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE, related_name="bookmarks")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="help_bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("request", "user")


class Report(models.Model):
    request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE, related_name="reports")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="help_reports")
    reason = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)


class Team(models.Model):
    request = models.OneToOneField(HelpRequest, on_delete=models.CASCADE, related_name="team")
    created_at = models.DateTimeField(auto_now_add=True)


class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="team_memberships")
    approved = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("team", "user")


class ChatMessage(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_team_messages")
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
