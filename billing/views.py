from django.shortcuts import render, redirect, get_object_or_404
from .models import MembershipPlan, Payment, Member
from .forms import MembershipPlanForm, PaymentForm, MemberForm


def billing_dashboard(request):
    total_payments = Payment.objects.count()
    paid_payments = Payment.objects.filter(payment_status='Paid').count()
    pending_payments = Payment.objects.filter(payment_status='Pending').count()
    unpaid_payments = Payment.objects.filter(payment_status='Unpaid').count()

    context = {
        'total_payments': total_payments,
        'paid_payments': paid_payments,
        'pending_payments': pending_payments,
        'unpaid_payments': unpaid_payments,
    }
    return render(request, 'billing/dashboard.html', context)


def member_list(request):
    members = Member.objects.all().order_by('full_name')
    return render(request, 'billing/member_list.html', {'members': members})


def add_member(request):
    form = MemberForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('member_list')
    return render(request, 'billing/member_form.html', {'form': form})


def plan_list(request):
    plans = MembershipPlan.objects.all().order_by('plan_name')
    return render(request, 'billing/plan_list.html', {'plans': plans})


def add_plan(request):
    form = MembershipPlanForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('plan_list')
    return render(request, 'billing/plan_form.html', {'form': form})


def payment_list(request):
    payments = Payment.objects.select_related('member', 'membership_plan').all().order_by('-created_at')

    selected_status = request.GET.get('status')
    selected_member = request.GET.get('member')

    if selected_status:
        payments = payments.filter(payment_status=selected_status)

    if selected_member:
        payments = payments.filter(member__full_name__icontains=selected_member)

    return render(request, 'billing/payment_list.html', {
        'payments': payments,
        'selected_status': selected_status,
        'selected_member': selected_member,
    })


def add_payment(request):
    form = PaymentForm(request.POST or None)

    if form.is_valid():
        payment = form.save(commit=False)

        if not payment.amount:
            payment.amount = payment.membership_plan.price

        payment.save()
        return redirect('payment_list')

    return render(request, 'billing/payment_form.html', {'form': form})


def receipt_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'billing/receipt.html', {'payment': payment})