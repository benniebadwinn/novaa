from django import forms

from .models import Contact, Newsletter, Subscriptions, Gstarted

from django.utils.translation import gettext_lazy as _
# from account.forms import SignupForm
#from users.models import Address,PickupStation
# from account.models import *
from django.contrib.auth import get_user_model
from django.forms import HiddenInput
from django import forms

# from account.models import subscriptions
import re

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ['first_name','subject', 'email_address', 'message']





class GstartedForm(forms.ModelForm):
    SERVICE_CHOICES = [
        ('Type Of Service', 'Type Of Service'),
        ('Pest Control-2', 'Home Cleaning'),
        ('Pest Control-3', 'Carpet Cleaning'),
    ]
    service_type = forms.ChoiceField(choices=SERVICE_CHOICES, widget=forms.Select(attrs={'class': 'form-select p-3 border-0'}))
    
    class Meta:
        model = Gstarted
        fields = ['name', 'phone', 'email_address', 'service_type']





class NewsletterForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=Subscriptions.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    send_to_all = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Newsletter
        fields = ['subject', 'content', 'recipients', 'send_to_all']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically set the choices for the recipients field
        self.fields['recipients'].queryset = Subscriptions.objects.all()

        # Hide the recipients field when send_to_all is selected
        if self.initial.get('send_to_all', False):
            self.fields['recipients'].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super().clean()
        send_to_all = cleaned_data.get('send_to_all')
        recipients = cleaned_data.get('recipients')

        if not send_to_all and not recipients:
            # Raise a validation error if no recipients are selected
            raise forms.ValidationError("No recipients selected. The newsletter will not be sent.")

        if send_to_all:
            # If send_to_all is selected, clear the recipients field
            cleaned_data['recipients'] = []

        return cleaned_data
