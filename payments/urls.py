from django.urls import path
from .views import payment_selection, create_checkout, payment_success, payment_cancelled, checkout, initiate_mpesa_payment

app_name = 'payments'

urlpatterns = [
    path('payment-selection/', payment_selection, name='payment_selection'),
    path('create_checkout/', create_checkout, name='create_checkout'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),
    path('checkout/', checkout, name='checkout'),
    path('initiate_mpesa_payment/', initiate_mpesa_payment, name='initiate_mpesa_payment'),
]