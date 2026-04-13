from django import forms
from django.contrib.auth.models import User
from .models import MemberProfile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    fitness_goal = forms.CharField(max_length=100)
    experience_level = forms.ChoiceField(
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
        ]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        MemberProfile.objects.create(
            user=user,
            fitness_goal=self.cleaned_data['fitness_goal'],
            experience_level=self.cleaned_data['experience_level']
        )

        return user