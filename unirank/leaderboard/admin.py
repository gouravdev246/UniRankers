from django.contrib import admin
from .models import Achievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "title", "points", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "details", "user__name", "user__email")
