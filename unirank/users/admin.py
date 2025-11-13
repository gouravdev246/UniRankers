from django.contrib import admin
from .models import User, ContactMessage

# Register your models here.
from .models import User

admin.site.register(User)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
