from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='admin')
    
    # Resolving conflicts with default Django User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Property(models.Model):
    PROPERTY_TYPES = (
        ('House', 'House'),
        ('Flat', 'Flat'),
        ('Land', 'Land'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Sold', 'Sold'),
    )

    title = models.CharField(max_length=200, default="Untitled Property")
    description = models.TextField(default="No description provided.")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='House')
    city = models.CharField(max_length=100, default="Unknown City")
    address = models.TextField(default="No address provided.")
    image = models.ImageField(upload_to='property_images/', default='default_property.jpg')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    contact_phone = models.CharField(max_length=20, default="0000000000")
    contact_email = models.EmailField(default="noemail@example.com")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        verbose_name_plural = "Properties"
