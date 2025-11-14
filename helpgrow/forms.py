from django import forms
from .models import HelpRequest, RequestComment


class HelpRequestForm(forms.ModelForm):
    class Meta:
        model = HelpRequest
        fields = [
            "title",
            "request_type",
            "description",
            "required_skills",
            "urgency",
            "tags",
        ]

    def clean(self):
        cleaned = super().clean()
        for f in ["title", "request_type", "description", "urgency"]:
            if not cleaned.get(f):
                self.add_error(f, "This field is required.")
        return cleaned


class RequestCommentForm(forms.ModelForm):
    class Meta:
        model = RequestComment
        fields = ["content"]

    def clean_content(self):
        c = (self.cleaned_data.get("content") or "").strip()
        if not c:
            raise forms.ValidationError("Empty")
        if len(c) > 500:
            raise forms.ValidationError("Too long")
        return c
