from django.urls import path,include
from nova_main import views
from django.conf import settings
from django.conf.urls.static import static
from nova_main.views import ContactView, IndexView, SendNewsletterView, GstartedView





app_name = 'nova_main'


urlpatterns = [
    
    path('productpage/<int:product_id>/',views.productpage,name='productpage'),
    path('', IndexView.as_view(), name='index'),
    path('contact',ContactView.as_view(),name='contact'),
    path('gstarted/',GstartedView.as_view(),name='gstarted'),
    path('error_page',views.error_page,name='error_page'),
    path('about',views.about,name='about'),
    path('service',views.service,name='service'),
    path('projects',views.projects,name='projects'),
    path('prices',views.prices,name='prices'),
    path('subscribe/',views.subscribe, name="subscribe"),
    path('send/', SendNewsletterView.as_view(), name='send_newsletter'),
    # path('about',AboutView.as_view(),name='about'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)