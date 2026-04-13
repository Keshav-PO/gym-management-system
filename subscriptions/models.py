from django.db import models
from django.contrib.auth.models import User


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_months = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Subscription(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.member.username} - {self.plan.name}"