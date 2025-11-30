from django import forms
from .models import TestDriveRequest, Dealer
from django.utils import timezone
from datetime import time, datetime

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
    # ฟิลด์สำหรับรับค่าเฉพาะวัน (Date) ที่ผู้ใช้เลือก
    confirmation_datetime = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d' 
        ),
        required=False, 
        label='Confirmed Date'
    )
    
    class Meta:
        model = TestDriveRequest
        fields = [
            'status', 
            'confirmation_datetime', 
            'staff_notes'
        ]

    # ✅ เพิ่มเมธอด clean เพื่อรวมวันกับเวลา 01:00 AM
    def clean_confirmation_datetime(self):
        # รับค่าวันที่ที่ผู้ใช้ป้อนเข้ามา (เป็น date object)
        confirmed_date = self.cleaned_data.get('confirmation_datetime')
        
        if confirmed_date:
            # 1. กำหนดเวลาที่ต้องการเป็น 07:00:00 AM
            default_time = time(hour=7, minute=0, second=0)
            
            # 2. รวม Date object กับ Time object เป็น Naive Datetime
            naive_datetime = datetime.combine(confirmed_date, default_time)
            
            # 3. แปลงเป็น Timezone Aware Object (สำคัญมากสำหรับ Django)
            #    โดยถือว่า 07:00 AM นี้อยู่ใน TIME_ZONE ที่กำหนดใน settings.py (เช่น Asia/Bangkok)
            #    สิ่งนี้ช่วยแก้ปัญหา "วันแสดงไม่ตรงกัน"
            aware_datetime = timezone.make_aware(naive_datetime)
            
            return aware_datetime
            
        return confirmed_date # ถ้าผู้ใช้ไม่เลือกวัน ให้ส่งค่า None กลับไป  

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