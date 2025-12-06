from django import forms
from .models import ChapterSubmission

class ChapterSubmissionForm(forms.ModelForm):
    class Meta:
        model = ChapterSubmission
        fields = ['subject', 'chapter_name', 'student_drive_link']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Physics'}),
            'chapter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Optics'}),
            'student_drive_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://drive.google.com/...'}),
        }

class TeacherResponseForm(forms.ModelForm):
    class Meta:
        model = ChapterSubmission
        fields = ['teacher_notes_link']
        widgets = {
            'teacher_notes_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://drive.google.com/...'}),
        }
