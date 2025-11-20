# /Users/dew_ey/Desktop/Project/accounts/forms.py

from django import forms
# ต้อง import UserCreationForm และ UserChangeForm จาก auth.forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm 
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # เพิ่มฟิลด์ role และ dealer เข้าไปในฟิลด์พื้นฐานของ UserCreationForm
        fields = UserCreationForm.Meta.fields + ('role', 'dealer',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields