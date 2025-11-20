# blog/urls.py
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views import (HomePageView, HistoryPageView
                    , ContactPageView, CarsPageView, TestDriveCreateView
                    , DealerListView, DealerCreateView, DealerUpdateView
                    , DealerDeleteView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('company-history/', HistoryPageView.as_view(), name='history'),
    path('contact-us/', ContactPageView.as_view(), name='contact'),
    path('cars/', CarsPageView.as_view(), name='cars'),
    path('test-drive/', TestDriveCreateView.as_view(), name='testdrive'),
    path('dealers-list/', DealerListView.as_view(), name='dealer_list'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('test-drives/list/', views.TestDriveListView.as_view(), name='testdrive_list'),
    path('test-drives/edit/<int:pk>/', views.TestDriveUpdateView.as_view(), name='testdrive_update'),
    path('dealers/add/', DealerCreateView.as_view(), name='dealer_create'),
    path('dealers/edit/<int:pk>/', DealerUpdateView.as_view(), name='dealer_update'),
    path('dealers/delete/<int:pk>/', DealerDeleteView.as_view(), name='dealer_delete'),
    path('test-drive/success/', views.test_drive_success_view, name='test_drive_success'),
    ]
