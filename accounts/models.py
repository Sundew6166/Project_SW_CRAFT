from django.contrib.auth.models import AbstractUser
from django.db import models
from project.models import Dealer

class CustomUser(AbstractUser):
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('dealer', 'Dealer'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='dealer',
        verbose_name='Dealer'
    )

    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        related_name='users',
        verbose_name='ตัวแทนจำหน่าย'
    )

    def __str__(self):
        return self.username