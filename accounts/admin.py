# /Users/dew_ey/Desktop/Project/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # นำเข้า UserAdmin พื้นฐาน
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    # 1. กำหนดฟอร์มที่จะใช้ในการ 'เพิ่ม' ผู้ใช้ใหม่
    add_form = CustomUserCreationForm
    # 2. กำหนดฟอร์มที่จะใช้ในการ 'แก้ไข' ผู้ใช้ที่มีอยู่
    form = CustomUserChangeForm
    
    # 3. กำหนดฟิลด์ที่จะแสดงในหน้ารายการ (List View)
    list_display = ['username', 'email', 'role', 'dealer', 'is_staff']
    # เพิ่มตัวกรอง (Filter)
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']
    
    # 4. กำหนดกลุ่มฟิลด์สำหรับหน้า 'เพิ่ม' ผู้ใช้ (Add Form)
    # เราจะเพิ่มฟิลด์ 'role' และ 'dealer' เข้าไปในส่วนสุดท้ายของฟอร์ม
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'dealer',)}),
    )
    
    # 5. กำหนดกลุ่มฟิลด์สำหรับหน้า 'แก้ไข' ผู้ใช้ที่มีอยู่ (Change Form)
    # ค้นหา fieldsets เดิม และเพิ่มฟิลด์ของเราเข้าไป
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles and Dealer', {'fields': ('role', 'dealer',)}),
    )

# 6. ลงทะเบียน CustomUser Model ด้วย CustomUserAdmin ที่เรากำหนดเอง
admin.site.register(CustomUser, CustomUserAdmin)

# หมายเหตุ: ไม่จำเป็นต้อง Unregister User ถ้าคุณไม่เคย Register UserAdmin พื้นฐาน
# เนื่องจาก CustomUser จะใช้แทนที่ Default User โดยอัตโนมัติเมื่อตั้งค่า AUTH_USER_MODEL