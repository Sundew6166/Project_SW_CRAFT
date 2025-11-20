from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    
    list_display = ['username', 'email', 'role', 'dealer', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'dealer',)}),
    )
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles and Dealer', {'fields': ('role', 'dealer',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)