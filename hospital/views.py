from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import DoctorSignUpForm, PatientSignUpForm, PrescriptionForm
from .models import User, Prescription
import uuid

def home(request):
    return render(request, 'hospital/home.html', {'bg_image': 'hospital/images/home-bg.jpg'})

def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        form = DoctorSignUpForm()
    return render(request, 'hospital/signup.html', {'form': form, 'title': 'Doctor Sign Up', 'bg_image': 'hospital/images/doctor-bg.jpg'})

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'hospital/signup.html', {'form': form, 'title': 'Patient Sign Up', 'bg_image': 'hospital/images/patient-bg.jpg'})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_doctor:
                return redirect('doctor_dashboard')
            elif user.is_patient:
                return redirect('patient_dashboard')
        else:
            return render(request, 'hospital/login.html', {'error': 'Invalid credentials', 'bg_image': 'hospital/images/login-bg.jpg'})
    return render(request, 'hospital/login.html', {'bg_image': 'hospital/images/login-bg.jpg'})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor:
        return redirect('home')
    prescriptions = Prescription.objects.filter(doctor=request.user)
    return render(request, 'hospital/doctor_dashboard.html', {'prescriptions': prescriptions, 'bg_image': 'hospital/images/doctor-bg.jpg'})

@login_required
def patient_dashboard(request):
    if not request.user.is_patient:
        return redirect('home')
    prescriptions = Prescription.objects.filter(patient=request.user)
    return render(request, 'hospital/patient_dashboard.html', {'prescriptions': prescriptions, 'bg_image': 'hospital/images/patient-bg.jpg'})

@login_required
def create_prescription(request):
    if not request.user.is_doctor:
        return redirect('home')
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.share_id = str(uuid.uuid4())
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()
    return render(request, 'hospital/create_prescription.html', {'form': form, 'bg_image': 'hospital/images/doctor-bg.jpg'})

def view_prescription(request, share_id):
    prescription = get_object_or_404(Prescription, share_id=share_id)
    return render(request, 'hospital/view_prescription.html', {'prescription': prescription, 'bg_image': 'hospital/images/patient-bg.jpg'})
