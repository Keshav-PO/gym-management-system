from django import forms
from .models import GymClass


class GymClassForm(forms.ModelForm):
    class Meta:
        model = GymClass
        fields = ['title', 'class_date', 'class_time', 'capacity', 'description']
        widgets = {
            'class_date': forms.DateInput(attrs={'type': 'date'}),
            'class_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }