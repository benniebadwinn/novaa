import urllib.request

from . import pesapal_processor3

pesapal_processor3.consumer_key = "tgwvEFz6aTi4IGDyur1jZUzZ3rg4jTFH"
pesapal_processor3.consumer_secret = "wcumbpvE0zoX8tR68eXc9E6W/jI="
pesapal_processor3.testing = False


def post_transaction(Reference, FirstName, LastName, Email, PhoneNumber, Description, Amount, Type):

    post_params = {
        'oauth_callback': 'https://f9d5-154-159-237-38.ngrok-free.app/payment/oauth_callback1/'
    }

    request_data = {
        'Amount': str(Amount),
        'Description': Description,
        'Type': Type,
        'Reference': Reference,
        'PhoneNumber': str(PhoneNumber),
        'Email': Email,
        'FirstName': FirstName,
        'LastName': LastName
    }

    url = pesapal_processor3.postDirectOrder(post_params, request_data)

    return url




def post_transaction1(Reference,Description, Amount, Type):

    post_params = {
        'oauth_callback': 'https://f9d5-154-159-237-38.ngrok-free.app/payment/oauth_callback1/'
    }

    request_data = {
        'Amount': str(Amount),
        'Description': Description,
        'Type': Type,
        'Reference': Reference,

    }

    url = pesapal_processor3.postDirectOrder(post_params, request_data)

    return url


def get_detailed_order_status(merchant_reference, transaction_tracking_id):

    post_params = {
        'pesapal_merchant_reference': merchant_reference,
        'pesapal_transaction_tracking_id': transaction_tracking_id,
        # 'pesapal_payment': payment
    }
    url = pesapal_processor3.queryPaymentDetails(post_params)
    response = urllib.request.urlopen(url)

    return response.read()


def get_payment_status(merchant_reference, transaction_tracking_id):

    post_params = {
        'pesapal_merchant_reference': merchant_reference,
        'pesapal_transaction_tracking_id': transaction_tracking_id,
        # 'pesapal_payment': payment
    }
    url = pesapal_processor3.queryPaymentStatus(post_params)
    response = urllib.request.urlopen(url)

    return response.read()
