from django.urls import path
from . import views
# from payment.views import (PaymentView2)

app_name = 'payment'

urlpatterns = [
   
    path('pay/<int:product_id>/', views.payment, name='pay'),

    path('oauth_callback1/', views.callback1, name='callback'),
]