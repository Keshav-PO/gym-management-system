from django.urls import path
from . import views

urlpatterns = [
    path('', views.billing_dashboard, name='billing_dashboard'),
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.add_member, name='add_member'),

    path('plans/', views.plan_list, name='plan_list'),
    path('plans/add/', views.add_plan, name='add_plan'),

    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.add_payment, name='add_payment'),
    path('payments/receipt/<int:payment_id>/', views.receipt_view, name='receipt_view'),
]