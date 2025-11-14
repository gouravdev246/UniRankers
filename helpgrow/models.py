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
    urgency = models.CharField(maxlength=16)
    tags = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


