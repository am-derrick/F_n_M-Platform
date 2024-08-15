from django.urls import path
from .views import create_checkout, payment_success, payment_cancelled, checkout

urlpatterns = [
    path('create_checkout/', create_checkout, name='create_checkout'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),
    path('checkout/', checkout, name='checkout'),
]