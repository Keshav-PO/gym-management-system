from datetime import date
from calendar import monthrange

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import MembershipPlan, Subscription


def add_months(start_date, months):
    month = start_date.month - 1 + months
    year = start_date.year + month // 12
    month = month % 12 + 1
    day = min(start_date.day, monthrange(year, month)[1])
    return date(year, month, day)


def membership_plans(request):
    plans = MembershipPlan.objects.all()
    return render(request, 'subscriptions/membership_plans.html', {'plans': plans})


@login_required
def choose_plan(request, plan_id):
    plan = get_object_or_404(MembershipPlan, id=plan_id)

    Subscription.objects.filter(member=request.user, status='Active').update(status='Expired')

    start_date = date.today()
    end_date = add_months(start_date, plan.duration_months)

    Subscription.objects.create(
        member=request.user,
        plan=plan,
        end_date=end_date,
        status='Active'
    )

    return redirect('my_subscription')


@login_required
def my_subscription(request):
    subscription = Subscription.objects.filter(member=request.user, status='Active').order_by('-start_date').first()
    return render(request, 'subscriptions/my_subscription.html', {'subscription': subscription})