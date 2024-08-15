import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
import base64
from datetime import datetime

def get_mpesa_access_token():
    """gets the MPESA access token"""
    url = f"https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    mpesa_access_token = response.json()['access_token']
    return mpesa_access_token

def get_timestamp():
    """gets the timestamp and converts it to a specific format"""
    return datetime.now().strftime('%Y%m%d%H%M%S')

def generate_mpesa_password():
    """generates MPESA password and encodes it using base64"""
    timestamp = get_timestamp()
    data_to_encode = settings.MPESA_SHOTCODE + settings.MPESA_PASSKEY + timestamp
    encoded_string = base64.b64encode(data_to_encode.encode())
    return encoded_string.decode('utf-8')

def lipa_na_mpesa(phone_number, amount, account_ref, transaction_desc):
    """lipa na MPESA payment logic"""
    access_token = get_mpesa_access_token()
    api_url = f"https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": generate_mpesa_password(),
        "Timestamp": get_timestamp(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_ref,
        "TransactionDesc": transaction_desc
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()