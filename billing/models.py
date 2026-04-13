from django.db import models


class MembershipPlan(models.Model):
    plan_name = models.CharField(max_length=100)
    duration_in_months = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.plan_name} - ${self.price}"


class Member(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    joined_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Payment(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
        ('Pending', 'Pending'),
    ]

    METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_date = models.DateField()
    due_date = models.DateField()
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.member.full_name}"