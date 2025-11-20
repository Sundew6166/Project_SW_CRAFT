from django.contrib.auth.models import AbstractUser
from django.db import models
from project.models import Dealer

class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email Address'
    )

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('dealer', 'Dealer'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='dealer',
        verbose_name='Role'
    )

    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        related_name='users',
        verbose_name='Dealer Code'
    )

    def __str__(self):
        return self.username