from django.urls import path
from . import views

urlpatterns = [
    path('', views.class_list, name='class_list'),
    path('create/', views.class_create, name='class_create'),
    path('register/<int:class_id>/', views.register_class, name='register_class'),
    path('my-classes/', views.my_classes, name='my_classes'),
]