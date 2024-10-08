import json
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests.auth import HTTPBasicAuth
from .credentials import MpesaAccessToken, LipanaMpesaPpassword

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def ourwork(request):
    return render(request, 'ourwork.html')

def contact(request):
    return render(request, 'contact.html')

def support(request):
    return render(request, 'support.html')

def pay(request):
    return render(request, 'pay.html')

def token(request):
    consumer_key = '7sZhKcCCQ3CKzEX4obZ5fYS6MLYw4SPZwICVKVPk36ytXkAH'
    consumer_secret = 'G9tbHQWYPS8OXrRZ22GqPHtAjbSAD9G8LQlOBE3GthcOVQLE32PagqKbOvNFp6CV'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def stk(request):
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")