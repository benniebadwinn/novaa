from django.shortcuts import render
from .forms import ContactForm, NewsletterForm,GstartedForm
from django.views.generic import (
    DetailView,ListView,TemplateView,
    CreateView,UpdateView,DeleteView,ListView,FormView,View
)
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
# Esoko
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse ,HttpResponseForbidden ,JsonResponse
from nova_main.models import Product, Projects, Subscriptions, Gstarted
from django.views.generic import ListView
from django.contrib import messages
from datetime import datetime
from django.utils import timezone

# Create your views here.
def productpage(request, product_id):
    request.session['product_id'] = product_id
    return redirect('payment:pay', product_id=product_id)



class IndexView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Projects.objects.all()  # Add projects to the context
        return context



def about(request):
    return render(request, 'about.html')


def error_page(request):
    return render(request, 'error_page.html')


def service(request):
    return render(request, 'service.html')



def projects(request):
    return render(request, 'project.html')



def prices(request):
    return render(request, 'price.html')


# subscribe
def subscribe(request):
    try:
        email = request.POST['email']
    except KeyError:
        messages.error(request, "Email not provided.")
        return redirect("/")

    # Assuming the user is authenticated
    if request.user.is_authenticated:
        # Save the subscription with the current user
        subscription = Subscriptions(email=email)
        subscription.save()

        messages.success(request, "Subscription Added!")
    else:
        messages.error(request, "User not authenticated. Please log in.")

    return redirect("/")



class SendNewsletterView(View):
    template_name = 'send_newsletter.html'

    def get(self, request):
        form = NewsletterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            sender = request.user
            recipients = form.cleaned_data['recipients']

            print(f"Sender: {sender}")
            print(f"Recipients: {recipients}")

            newsletter = form.save(commit=False)
            newsletter.sender = sender
            newsletter.save()

            # Check if any recipients are selected or send_to_all is True
            if recipients or form.cleaned_data['send_to_all']:
                # Send the newsletter using Django's send_mail function
                subject = newsletter.subject
                message = newsletter.content
                recipient_emails = [user.email for user in recipients]

                try:
                    # Sending logic here (modify as per your requirements)
                    if form.cleaned_data['send_to_all']:
                        # Send the newsletter to all subscribers
                        recipient_emails = [subscriber.email for subscriber in Subscriptions.objects.all()]
                        send_mail(
                            subject,
                            message,
                            'sender@example.com',  # Replace with your actual sender email
                            recipient_emails,
                            fail_silently=False,
                        )
                    elif recipients:
                        # Send the newsletter to selected recipients
                        send_mail(
                            subject,
                            message,
                            'sender@example.com',  # Replace with your actual sender email
                            recipient_emails,
                            fail_silently=False,
                        )

                    # Mark the newsletter as sent after successfully sending
                    newsletter.sent_at = timezone.now()
                    newsletter.save()

                    # Display success message on the same page
                    messages.success(request, 'Newsletter sent successfully!')
                    return render(request, self.template_name, {'form': NewsletterForm()})

                except Exception as e:
                    print(f"An error occurred while sending the newsletter: {e}")
                    messages.error(request, f'Error sending newsletter. Details: {e}')

            else:
                # Handle the case when no recipients are selected
                print("No recipients selected. The newsletter will not be sent.")
                messages.warning(request, 'No recipients selected. The newsletter will not be sent.')

        return render(request, self.template_name, {'form': form})







class ContactView(CreateView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('nova_main:contact')

    def form_valid(self, form):
        if form.is_valid():
            try:
                form.instance.user = self.request.user  # Set the user field if it exists in your Contact model
                form.save()
                self.send_mail(form)
            except Exception as e:
                print("Error saving form data:", e)
        else:
            print("Form is not valid:", form.errors)
        return super().form_valid(form)

    def send_mail(self, form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        from_email = form.cleaned_data['email_address']

        to_email = [settings.DEFAULT_FROM_EMAIL]
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, to_email)
                print("Email sent successfully.")
            except BadHeaderError as e:
                print("Error sending email:", e)
                return HttpResponse('Invalid header found.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us'
        return context
    




class GstartedView(CreateView):
    template_name = 'index.html'
    form_class = GstartedForm
    success_url = reverse_lazy('nova_main:index')

    def form_valid(self, form):
        if form.is_valid():
            try:
                # form.instance.user = self.request.user  # Uncomment if you have a user field in your model
                form.save()
                self.send_mail(form)
            except Exception as e:
                print("Error saving form data:", e)
        else:
            print("Form is not valid:", form.errors)
        return super().form_valid(form)

    def send_mail(self, form):
        subject = 'New Service Inquiry'
        
        # Get the display label for the service_type
        service_type_display = dict(form.fields['service_type'].choices).get(form.cleaned_data['service_type'])

        message = (
            f"A new service inquiry has been received.\n\n"
            f"Name: {form.cleaned_data['name']}\n"
            f"Phone: {form.cleaned_data['phone']}\n"
            f"Email: {form.cleaned_data['email_address']}\n"
            f"Service Type: {service_type_display}"
        )
        from_email = form.cleaned_data['email_address']
        to_email = [settings.DEFAULT_FROM_EMAIL]
        try:
            send_mail(subject, message, from_email, to_email)
            print("Email sent successfully.")
        except BadHeaderError as e:
            print("Error sending email:", e)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us'
        return context


