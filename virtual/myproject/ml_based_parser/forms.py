from django import forms
from .models import ResumeParse


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = ResumeParse
        fields = ('candidate_id', 'document',)
