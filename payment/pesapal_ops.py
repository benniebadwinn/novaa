from . import pesapal_processor


def post_transaction(Reference, FirstName, LastName, Email, PhoneNumber, Description, Amount, Type):
    oauth_consumer_key = "tgwvEFz6aTi4IGDyur1jZUzZ3rg4jTFH"
    oauth_consumer_secret = "wcumbpvE0zoX8tR68eXc9E6W/jI="
    oauth_callback = "https://f9d5-154-159-237-38.ngrok-free.app/payment/oauth_callback1/"

    pesapal = pesapal_processor.PesaPal(oauth_consumer_key, oauth_consumer_secret, 'production')
    pesapal.reference = Reference
    pesapal.last_name = LastName
    pesapal.first_name = FirstName
    pesapal.amount = Amount
    pesapal.type_=Type
    pesapal.description=Description
    pesapal.phone_number = PhoneNumber
    pesapal.email = Email
    pesapal.callback_url = oauth_callback
    iframe_src = pesapal.generate_iframe_src()
    return iframe_src