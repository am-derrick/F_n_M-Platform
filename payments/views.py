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
from .utils import lipa_na_mpesa
import json

# stripe settings
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment_selection(request):
    """Renders the payment selection page"""
    return render(request, 'payments/payment_selection.html')

@login_required
def create_checkout(request):
    """creates session on stripe payment checkout
    also checks if there's an existing stripe coupon code"""

@login_required
def create_checkout(request):
    """Creates session on stripe payment checkout or grants access with a valid coupon"""
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')

        if not coupon_code:
            messages.error(request, "Please enter a coupon code.")
            return redirect('payments:payment_selection')

        # Manually check if the coupon is 'INTERVIEW20'
        if coupon_code == 'INTERVIEW20':
            # Update user to full_member
            user = CustomUser.objects.get(username=request.user.username)
            user.is_full_member = True
            user.save()

            messages.success(request, "Coupon applied successfully! You now have full membership access.")
            return redirect('macroeconomics:inflation_trend')
        else:
            messages.error(request, "Invalid coupon code.")
            return redirect('payments:payment_selection')

    return render(request, 'payments/payment_selection.html')


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

@login_required
def initiate_mpesa_payment(request):
    """initiates MPESA payment"""
    if request.method == 'POST':
        data = json.loads(request.body)  # Load the JSON data sent in the request
        phone_number = data.get('phone_number')
        amount = 1000
        account_ref = "Full Membership"
        transaction_desc = "Payment for Full Membership"

        response = lipa_na_mpesa(phone_number, amount, account_ref, transaction_desc)

        if response.get('ResponseCode') == '0':
            return JsonResponse({"message": "Success! Please complete the payment on your phone."})
        else:
            return JsonResponse({"message": "Payment initiation failed."})
    return render(request, 'payments/initiate_mpesa_payment.html')

@csrf_exempt
def mpesa_webhook(request):
    """Listens for MPESA payment and updates user membership"""
    if request.method == 'POST':
        mpesa_data = json.loads(request.body)

        # Extract relevant information
        phone_number = mpesa_data.get("Body", {}).get("stkCallback", {}).get("CallbackMetadata", {}).get("Item", [{}])[4].get("Value")
        result_code = mpesa_data.get("Body", {}).get("stkCallback", {}).get("ResultCode")

        if result_code == 0:
            user = request.user
            user.is_full_member = True
            user.save()

            return JsonResponse({"status": "success", "message": "Membership upgraded."})
        else:
            return JsonResponse({"status": "error", "message": "Payment failed."})


    return JsonResponse({"status": "error", "message": "Invalid request method."})