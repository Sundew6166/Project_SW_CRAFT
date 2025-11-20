from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled'),
]

CAR_MODEL_CHOICES = [
    ('', '--- Select Car Model ---'),
    ('XFORCE HEV', 'XFORCE HEV'),
    ('Pajero Sport', 'New Pajero Sport'),
    ('Triton', 'TRITON'),
    ('Xpander HEV', 'Xpander HEV'),
    ('Xpander Cross HEV', 'Xpander Cross HEV'),
    ('Attrage', 'Attrage'),
    ('Mirage', 'Mirage'),
]

# -------------------------------------------------------------
# 1. Dealer Model
# -------------------------------------------------------------
class Dealer(models.Model):
    name = models.CharField(max_length=150, verbose_name="Dealer Name")
    address = models.TextField(verbose_name="Full Address")
    dealer_code = models.CharField(
        max_length=10, 
        unique=True,
        verbose_name='Dealer Code'
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    class Meta:
        verbose_name = "Dealer"
        verbose_name_plural = "Dealer"

    def __str__(self):
        return f"{self.name}"

# -------------------------------------------------------------
# 3. TestDriveRequest Model
# -------------------------------------------------------------
class TestDriveRequest(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    car_model = models.CharField(
        max_length=50,
        choices=CAR_MODEL_CHOICES,
        default=''
    )
    preferred_date = models.DateField()
    
    preferred_dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name='test_drive_requests',
        verbose_name='Preferred Dealer',
        to_field='dealer_code',
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    confirmation_staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='testdrive_confirmations',
    )
    
    confirmation_datetime = models.DateTimeField(null=True, blank=True)
    staff_notes = models.TextField(blank=True, verbose_name="Dealer Notes")
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        return f"Request for {self.car_model} by {self.full_name} ({self.status})"