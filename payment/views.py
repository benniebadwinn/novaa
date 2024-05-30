import json
import random
import string
import logging 
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from . import pesapal_ops3
from django.shortcuts import render, get_object_or_404, redirect
from . import forms
from .models import Payment
from nova_main.models import Product
# from moontag_app.models import Address, OrderItem, Order

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.db import connection
from django.db.models import F
from django.db import transaction, models
from django.views.generic.base import View
from decimal import Decimal

from django.http import JsonResponse



def payment(request, product_id):
    account_reference = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    total_cost = 0
    order = None  # Set a default value
   
    if request.method == 'POST':
        form = forms.Payment(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.reference = account_reference
            payment.type = 'MERCHANT'
            payment.description = 'product purchased'
            Reference = payment.reference
            FirstName = payment.first_name
            LastName = payment.last_name
            Email = payment.email
            PhoneNumber = payment.phone
            Description = payment.description
            Amount = payment.amount
            Type = payment.type
            payment.save()
            iframe_src = pesapal_ops3.post_transaction(Reference, FirstName, LastName, Email, PhoneNumber, Description, Amount, Type)

            print(iframe_src)

            return render(request, 'payment/paynow.html', {'iframe_src': iframe_src})

    else:
        product_id = request.session['product_id']
        product = get_object_or_404(Product, id=product_id)
        total_cost = product.price 
        print(product.price)

        form = forms.Payment()

    
    context = {'amount': total_cost,'form': form,'product_id': product_id}

    return render(request, 'payment/index.html', context)





@csrf_exempt
def callback1(request):
    if request.method == 'POST':
        print(request.body)
        print('POST')
    else:
        params = request.GET
        print(params)
    
    merchant_reference = params.get('pesapal_merchant_reference')
    transaction_tracking_id = params.get('pesapal_transaction_tracking_id')
    
    # Check if merchant_reference and transaction_tracking_id are not None
    if merchant_reference and transaction_tracking_id:
        # Get payment status
        status = pesapal_ops3.get_payment_status(merchant_reference, transaction_tracking_id).decode('utf-8')
        p_status = str(status).split('=')[1]

        # Print p_status
        print('Payment status:', p_status)

        # Check if pesapal status is COMPLETED
        if p_status == 'COMPLETED':
            # Check if the payment exists
            try:
                payment = Payment.objects.get(reference=merchant_reference)
            except Payment.DoesNotExist:
                # If no payment exists, handle accordingly or log an error
                return redirect('error_page')  # Redirect to an error page or handle accordingly
            
            # Update payment status to True
            payment.paid = True
            payment.save()

            # Save merchant_reference and transaction_tracking_id to the Payment model
            payment.merchant_reference = merchant_reference
            payment.transaction_tracking_id = transaction_tracking_id
            payment.save()
        
            # Add a success message
            messages.success(request, 'Payment was successfully completed!')

            # Redirect to a success page or return a success response
            return redirect('nova_main:index')
    else:
        # Redirect to an error page or return an error response
        return redirect('nova_main:error_page')  # Replace 'shop:home' with your actual URL name
    
    # Add a failure message or return a failure response if needed
    messages.error(request, 'Insufficient funds.')
    return HttpResponse(status=400)  # Bad Request
