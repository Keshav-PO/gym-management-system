from django.contrib import admin
from .models import Member, MembershipPlan, Payment


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'joined_on')
    search_fields = ('full_name', 'email')


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'duration_in_months', 'price')
    search_fields = ('plan_name',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'member',
        'membership_plan',
        'amount',
        'billing_date',
        'due_date',
        'payment_status',
        'payment_method',
    )
    list_filter = ('payment_status', 'payment_method', 'billing_date')
    search_fields = ('member__full_name', 'membership_plan__plan_name')