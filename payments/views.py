import stripe
import stripe.error
from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.models import CustomUser
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# stripe settings
stripe.api_key = settings.STRIPE_SECRET_KEY

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

@login_required
def checkout(request):
    """Renders pre-payment checkout page with Stripe payment form"""
    context = {
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'payments/checkout.html', context)

@csrf_exempt
def payment_success(request):
    """Handles payment success logic"""
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=request.user.username)
        user.is_full_member = True
        user.save()

        messages.success(request, 'Thank you for subscribing to our full membership!')
        return redirect('macroeconomics:inflation_trend')
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
