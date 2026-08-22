from django import forms

from .models import CommunityPost, CommunityReply, CommunityReport


class CommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ["title", "category", "city", "body"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "What do you want to talk about?", "maxlength": 180}),
            "category": forms.Select(),
            "city": forms.Select(),
            "body": forms.Textarea(attrs={"rows": 8, "placeholder": "Share the context, route, question or tip..."}),
        }

    def clean_title(self):
        title = " ".join(self.cleaned_data["title"].split())
        if len(title) < 8:
            raise forms.ValidationError("Give your post a little more context.")
        return title

    def clean_body(self):
        body = self.cleaned_data["body"].strip()
        if len(body) < 20:
            raise forms.ValidationError("Please add at least a little detail so other travellers can help.")
        return body


class CommunityReplyForm(forms.ModelForm):
    class Meta:
        model = CommunityReply
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4, "placeholder": "Share your experience or suggestion..."}),
        }

    def clean_body(self):
        body = self.cleaned_data["body"].strip()
        if len(body) < 3:
            raise forms.ValidationError("Write a little more before posting your reply.")
        return body


class CommunityReportForm(forms.ModelForm):
    class Meta:
        model = CommunityReport
        fields = ["reason", "note"]
        widgets = {
            "note": forms.Textarea(attrs={"rows": 3, "placeholder": "Optional context"}),
        }
