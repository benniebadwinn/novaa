from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from nova_main.models import Contact, Product, Projects, Subscriptions, Newsletter, Gstarted

# Register your models here.
admin.site.register(Contact)
admin.site.register(Projects)
admin.site.register(Subscriptions)
admin.site.register(Product)
admin.site.register(Newsletter)
admin.site.register(Gstarted)