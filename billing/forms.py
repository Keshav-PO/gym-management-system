from django import forms
from .models import MembershipPlan, Payment, Member


class MembershipPlanForm(forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ['plan_name', 'duration_in_months', 'price', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['full_name', 'email', 'phone_number']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'member',
            'membership_plan',
            'amount',
            'billing_date',
            'due_date',
            'payment_method',
            'payment_status',
            'notes',
        ]
        widgets = {
            'billing_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }