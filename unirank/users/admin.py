from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import ContactMessage

# Register your models here.
User = get_user_model()

admin.site.register(User)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
