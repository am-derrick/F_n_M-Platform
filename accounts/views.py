import stripe
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from .models import CustomUser

# stripe settings
stripe.api_key = settings.STRIPE_SECRET_KEY

def signup(request):
    """sign up/register view"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html',  {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'

@login_required
def home(request):
    """home view"""
    return redirect('macroeconomics:home')

@login_required
def create_checkout(request):
    """creates session on stripe payment checkout"""
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Full Membership',
                },
                'unit_amount': 1000,
            },
            'quantity': 1
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/accounts/payment_success'),
        cancel_url=request.build_absolute_uri('/accounts/payment_cancelled'),
    )
    return JsonResponse({'id': session.id})

@csrf_exempt
def payment_success(request):
    """Handles payment success logic"""
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=request.user.username)
        user.is_full_member = True
        user.save()
    return redirect('macroeconomics:home')

@csrf_exempt
def payment_cancelled(request):
    """handles payment cancellation"""
    return redirect('macroeconomics:home')