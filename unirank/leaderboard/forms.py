from django import forms
from .models import Achievement


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = [
            "category",
            "title",
            "details",
            "value",
            "cgpa",
            "certificate_image",
        ]

    def clean(self):
        cleaned = super().clean()
        category = cleaned.get("category")
        cgpa = cleaned.get("cgpa")
        cert_img = cleaned.get("certificate_image")
        title = cleaned.get("title")
        value = cleaned.get("value")

        if category == Achievement.CATEGORY_CGPA and cgpa is None:
            self.add_error("cgpa", "CGPA is required for CGPA achievements.")
        if category == Achievement.CATEGORY_CERTIFICATION and cert_img is None:
            self.add_error("certificate_image", "Certificate image is required for certifications.")
        if category in (Achievement.CATEGORY_CERTIFICATION, Achievement.CATEGORY_SKILL, Achievement.CATEGORY_BADGE):
            if not title:
                self.add_error("title", "Title is required for this category.")
            if not value:
                self.add_error("value", "This field is required for this category.")
        return cleaned
