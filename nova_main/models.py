from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.urls import reverse


# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Set unique=True to ensure unique slugs
    Service = models.CharField(max_length=100, blank=True, null=True)
    img = models.ImageField(upload_to="media/product_images/%Y/%m/%d",)
    price = models.PositiveBigIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



    class Meta:
        verbose_name_plural = '1. Products'
        ordering = ['title']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['title']),
            models.Index(fields=['-created']),
        ]


    def __str__(self):
        return self.title
    


    def image_tag(self):
        return mark_safe('<img src="%s" width="60" height="60" />' % (self.img.url))


    def get_absolute_url(self):
            return reverse('shop:product_detail',
                           args=[self.id, self.slug])


    def save(self, *args, **kwargs):
        if not self.slug:  # Only set the slug if it hasn't been set
            self.slug = slugify(self.title)
            # Ensure the slug is unique by appending a number if necessary
            original_slug = self.slug
            queryset = Product.objects.filter(slug=self.slug).exists()
            counter = 1
            while queryset:
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                queryset = Product.objects.filter(slug=self.slug).exists()
        super().save(*args, **kwargs)


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=150)
    message = models.TextField(max_length=2000)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name='Contact'
        verbose_name_plural = '2. Contacts'

class Gstarted(models.Model):
    SERVICE_CHOICES = [
        ('Type Of Service', 'Type Of Service'),
        ('Pest Control-2', 'Home Cleaning'),
        ('Pest Control-3', 'Carpet Cleaning'),
    ]
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='Type Of Service')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=150)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'gstarted'
        verbose_name_plural = '3. gstarted'


class Projects(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to="media/product_images/%Y/%m/%d",)
    created = models.DateTimeField(auto_now_add=True)
 

    class Meta:
        verbose_name_plural = '4. Projects'
        ordering = ['title']



    def __str__(self):
        return self.title
    


    def image_tag(self):
        return mark_safe('<img src="%s" width="60" height="60" />' % (self.img.url))
    


class Subscriptions(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = '5. Subscriptions'
        ordering = ['email']

class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(Subscriptions, related_name='newsletters_sent')

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.recipients.exists():
            all_subscribers = Subscriptions.objects.all()
            self.recipients.set(all_subscribers)
        super().save(*args, **kwargs)


    class Meta:
        verbose_name='Newsletter'
        verbose_name_plural = '6. Newsletter'

