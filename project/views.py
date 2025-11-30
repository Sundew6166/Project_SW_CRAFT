from django.utils import timezone
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView

from config import settings
from .models import TestDriveRequest, Dealer, TestDriveRequest
from .forms import TestDriveForm, TestDriveUpdateForm, DealerForm, DealerUpdateForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser

class HomePageView(TemplateView):
    template_name = 'home.html'

class HistoryPageView(TemplateView):
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["timeline_data"] = [
            ("1961", "Foundation of SMC",
             "Sittipol Motor Co., Ltd. was established as the sole distributor of Mitsubishi vehicles."),
            ("1964", "UDMI Established",
             "United Development Motor Industry Co., Ltd. began automobile assembly operations."),
            ("1987", "MMC Sittipol Founded",
             "The merger marked the beginning of manufacturing for global markets."),
            ("1988", "First Export – Lancer Champ",
             "The first Thai-made Mitsubishi exported to Canada."),
            ("1996", "Laem Chabang Plant 2",
             "Major production site for 1-ton pickup trucks."),
            ("2018", "Education Academy",
             "Modern training center for engineers & technicians."),
            ("2021", "60th Anniversary",
             "Celebration of 6 million-unit production milestone."),
        ]

        return ctx
    
class ContactPageView(TemplateView):
    template_name = 'contact.html'

class CarsPageView(TemplateView):
    template_name = 'cars.html'

class TestDriveCreateView(CreateView):
    model = TestDriveRequest 
    form_class = TestDriveForm 

    template_name = 'test_drive.html' 
    
    def get_success_url(self):
        return reverse('test_drive_success') 

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
        
def test_drive_success_view(request):
    """View to display the test drive success confirmation page."""
    return render(request, 'test_drive_success.html')
    
class DealerListView(ListView):
    model = Dealer
    template_name = 'dealer_list.html' 
    context_object_name = 'dealer_list' 
    
    def get_queryset(self):
        return Dealer.objects.filter(is_active=True).order_by('name')
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    
@login_required
def test_drive_list_view(request):
    requests = TestDriveRequest.objects.all()
    context = {'requests': requests}
    return render(request, 'test_drive_list.html', context)

class TestDriveListView(LoginRequiredMixin, ListView):
    model = TestDriveRequest
    template_name = 'test_drive_list.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        
        if user.is_authenticated:
            # 1. Admin/Superuser เห็นทั้งหมด
            # ใช้ user.is_staff (ถ้าคุณใช้ StaffRequiredMixin) หรือ user.role == 'admin'
            if user.is_superuser or user.is_staff or user.role == 'admin':
                return TestDriveRequest.objects.all().order_by('-requested_at')
            
            # 2. Dealer เห็นเฉพาะของตัวเอง
            elif user.role == 'dealer':
                # ตรวจสอบว่าผู้ใช้ Dealer ถูกผูกกับสาขาแล้วหรือไม่
                if user.dealer:
                    # ดึง dealer_code จาก Dealer Model ที่เชื่อมโยง
                    user_dealer_code = user.dealer.dealer_code
                    
                    # 🚨 การกรอง: ต้องมั่นใจว่า preferred_dealer ใน TestDriveRequest เก็บ Dealer Code
                    return TestDriveRequest.objects.filter(
                        preferred_dealer=user_dealer_code
                    ).order_by('-requested_at')
                
                # ถ้าเป็น Dealer แต่ยังไม่ผูกกับสาขาใดๆ ก็ไม่เห็นอะไร
                return TestDriveRequest.objects.none()
        
        # ผู้ใช้ที่ไม่ได้เข้าสู่ระบบจะไม่เห็นอะไร (แต่ LoginRequiredMixin จัดการแล้ว)
        return TestDriveRequest.objects.none()

class TestDriveUpdateView(LoginRequiredMixin, UpdateView):
    model = TestDriveRequest
    form_class = TestDriveUpdateForm
    template_name = 'test_drive_update.html'
    success_url = reverse_lazy('testdrive_list')

    def form_valid(self, form):
        # 1. ให้ Django ดึงข้อมูลจากฟอร์มมาเตรียมไว้
        testdrive = form.save(commit=False)

        # 2. บันทึกว่าใครเป็นคนอัปเดต (ตั้งค่าอัตโนมัติ)
        testdrive.confirmation_staff = self.request.user

        # 4. บันทึกข้อมูลทั้งหมดลงฐานข้อมูล (รวมถึง confirmation_datetime ที่ผู้ใช้เลือก)
        testdrive.save()
        return super().form_valid(form)
    
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # return self.request.user.is_staff or self.request.user.is_superuser
        return self.request.user.is_superuser

class DealerCreateView(StaffRequiredMixin, CreateView):
    model = Dealer
    form_class = DealerForm
    template_name = 'dealer_create.html'
    success_url = reverse_lazy('dealer_list')

class DealerUpdateView(StaffRequiredMixin, UpdateView):
    model = Dealer
    form_class = DealerUpdateForm
    template_name = 'dealer_update.html' 
    success_url = reverse_lazy('dealer_list')

class DealerDeleteView(StaffRequiredMixin, DeleteView):
    model = Dealer
    template_name = 'dealer_confirm_delete.html'
    success_url = reverse_lazy('dealer_list')

class DealerUserCreateView(StaffRequiredMixin, CreateView):
    form_class = CustomUserCreationForm 
    template_name = 'dealer_user_create.html'
    success_url = reverse_lazy('user_list')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        
        user.role = 'dealer' 
        
        user.save()
        return super().form_valid(form)
    
class UserListView(StaffRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'user_list.html'
    
    def get_queryset(self):
        return CustomUser.objects.exclude(is_superuser=True).order_by('role', 'username')

class UserDeleteView(StaffRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj == self.request.user:
            raise PermissionDenied("You cannot delete your own account.")
        return obj