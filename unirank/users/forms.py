from django import forms
from .models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "profile_photo",
            "name",
            "phone_number",
            "cgpa",
            "course",
            "branch",
            "semester",
            "github_url",
            "linkedin_url",
            "instagram_url",
            "leetcode_url",
            "website_url",
        ]

    def clean_cgpa(self):
        cgpa = self.cleaned_data.get("cgpa")
        if cgpa is not None:
            if cgpa < 0 or cgpa > 10:
                raise forms.ValidationError("CGPA must be between 0 and 10.")
        return cgpa
