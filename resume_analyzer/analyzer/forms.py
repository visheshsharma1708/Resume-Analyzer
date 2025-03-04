from django import forms
from .models import Candidate

class ResumeUploadForm(forms.ModelForm):
    job_description = forms.CharField(widget=forms.Textarea, required=True)  # Extra field for job description

    class Meta:
        model = Candidate
        fields = ['name', 'email', 'phone', 'skills', 'experience', 'education', 'resume']
