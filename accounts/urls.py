from django.urls import path
from .views import home, signup, CustomLogoutView, CustomLoginView, create_checkout, payment_cancelled, payment_success

urlpatterns = [
    path('home/', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('create_checkout/', create_checkout, name='create_checkout'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),
]