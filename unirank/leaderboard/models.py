from django.db import models
from django.conf import settings


class Achievement(models.Model):
    CATEGORY_CERTIFICATION = "CERTIFICATION"
    CATEGORY_SKILL = "SKILL"
    CATEGORY_CGPA = "CGPA"
    CATEGORY_BADGE = "BADGE"
    CATEGORY_OTHER = "OTHER"

    CATEGORY_CHOICES = (
        (CATEGORY_CERTIFICATION, "Certification"),
        (CATEGORY_SKILL, "Skill"),
        (CATEGORY_CGPA, "CGPA"),
        (CATEGORY_BADGE, "Badge"),
        (CATEGORY_OTHER, "Other"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="achievements",
    )
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    value = models.CharField(max_length=64, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    semester = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 9)],
        blank=True,
        null=True,
    )
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    certificate_image = models.ImageField(upload_to="certificates/", blank=True, null=True)
    skill_level = models.CharField(
        max_length=16,
        blank=True,
        choices=(
            ("BEGINNER", "Beginner"),
            ("INTERMEDIATE", "Intermediate"),
            ("ADVANCED", "Advanced"),
        ),
    )
    skill_category = models.CharField(
        max_length=16,
        blank=True,
        choices=(
            ("TECHNICAL", "Technical"),
            ("SOFT", "Soft Skills"),
        ),
    )
    issuer = models.CharField(max_length=255, blank=True)
    earned_on = models.DateField(blank=True, null=True)
    points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-points", "-created_at"]

    def __str__(self):
        return f"{self.user} - {self.category} - {self.title} ({self.points})"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "achievement")


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

# Create your models here.
