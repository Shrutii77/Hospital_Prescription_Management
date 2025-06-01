from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctor_signup/', views.doctor_signup, name='doctor_signup'),
    path('patient_signup/', views.patient_signup, name='patient_signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('create_prescription/', views.create_prescription, name='create_prescription'),
    path('prescription/<str:share_id>/', views.view_prescription, name='view_prescription'),
]
