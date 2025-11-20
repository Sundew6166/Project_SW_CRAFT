from django import forms
from .models import TestDriveRequest, Dealer

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

class TestDriveForm(forms.ModelForm):
    car_model = forms.ChoiceField(
        choices=CAR_MODEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}) 
    )

    preferred_dealer = forms.ModelChoiceField(
        queryset=Dealer.objects.filter(is_active=True).order_by('name'),
        empty_label="--- Select Preferred Dealer ---",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    
    class Meta:
        model = TestDriveRequest
        fields = [
            'full_name', 
            'phone_number', 
            'email', 
            'car_model', 
            'preferred_dealer', 
            'preferred_date',
        ]
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class TestDriveUpdateForm(forms.ModelForm):
    class Meta:
        model = TestDriveRequest
        fields = [
            'status', 
            # 'confirmation_staff', 
            # 'confirmation_datetime', 
            'staff_notes'
        ]

class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = ['name', 'address', 'dealer_code'] 
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}), 
            'dealer_code': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DealerUpdateForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = ['name', 'address', 'dealer_code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), 
            'dealer_code': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            # 'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}), 
        }