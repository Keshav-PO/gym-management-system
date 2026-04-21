from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.membership_plans, name='plan_list'),
    path('choose-plan/<int:plan_id>/', views.choose_plan, name='choose_plan'),
    path('my-subscription/', views.my_subscription, name='my_subscription'),
]