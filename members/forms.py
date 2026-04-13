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
        help_texts = {
            'username': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['password'].help_text = ''

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


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField()
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
        fields = ['username', 'email']
        help_texts = {
            'username': '',
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['fitness_goal'].help_text = ''
        self.fields['experience_level'].help_text = ''

        self.fields['fitness_goal'].initial = self.current_user.memberprofile.fitness_goal
        self.fields['experience_level'].initial = self.current_user.memberprofile.experience_level

    def clean_username(self):
        username = self.cleaned_data['username']
        existing_user = User.objects.filter(username=username).exclude(id=self.current_user.id).first()
        if existing_user:
            raise forms.ValidationError('This username is already taken.')
        return username

    def save(self, user):
        user = super().save(commit=True)

        profile = user.memberprofile
        profile.fitness_goal = self.cleaned_data['fitness_goal']
        profile.experience_level = self.cleaned_data['experience_level']
        profile.save()

        return user