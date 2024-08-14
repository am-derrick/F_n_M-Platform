import stripe
from django.shortcuts import render, redirect
from django.contrib.auth import login
import stripe.error
from .forms import SignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from .models import CustomUser
import json
from django.http import HttpResponse

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

@csrf_exempt
def stripe_webhook(request):
    """stripe webhook logic, listens for stripe events and confirms
    membership on payment"""
    payload = request.body
    signature = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, signature, 'whsec_4155be881ecb8ec461a63d406f6c2db6afcb8b982f62bdabe2d3fa5ab5b05a02'
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    # Handles the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Updates user to full_member
        user = CustomUser.objects.get(username=session["client_reference_id"])
        user.is_full_member = True
        user.save()

        print(f"Payment succeeded for {user.username}")

    return JsonResponse({'status': 'success'})