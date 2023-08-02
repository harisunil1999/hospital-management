from django.shortcuts import render

# administration/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from administration.models import Admin

def create_admin(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=email, email=email, password=password)
        admin = Admin(user=user)
        admin.save()
        return redirect('admin_login')

    return render(request, 'create_admin.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None and user.admin:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'admin_login.html')


# administration/views.py


from .models import Department, Doctor, Patient, TimeSlot, Appointment
from django.contrib import messages

def appointment_form(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']
        date = request.POST['date']
        time_slot_id = request.POST['time_slot']
        doctor_id = request.POST['doctor']

        # Validate if the appointment is within clinic working hours
        # You can add your validation logic here

        # Validate if the appointment slot is available and not overlapping
        # You can add your validation logic here

        # Create the appointment
        patient = Patient.objects.create(name=name, email=email, phone=phone, place=place)
        doctor = Doctor.objects.get(id=doctor_id)
        time_slot = TimeSlot.objects.get(id=time_slot_id)
        appointment = Appointment.objects.create(
            patient=patient, doctor=doctor, date=date, time_slot=time_slot, status='pending'
        )
        messages.success(request, 'Appointment successfully scheduled! Waiting for approval.')
        return redirect('appointment_form')

    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    time_slots = TimeSlot.objects.all()
    context = {
        'departments': departments,
        'doctors': doctors,
        'time_slots': time_slots,
    }
    return render(request, 'appointment_form.html', context)


# administration/views.py

from django.shortcuts import render
from .models import Department, Doctor, TimeSlot, Appointment

def add_time_slots(request):
    if request.method == 'POST':
        day_of_week = request.POST['day_of_week']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        time_slot = TimeSlot.objects.create(day_of_week=day_of_week, start_time=start_time, end_time=end_time)
        messages.success(request, 'Time slot added successfully.')
        return redirect('add_time_slots')

    context = {}
    return render(request, 'add_time_slots.html', context)

def list_appointments(request):
    appointments = Appointment.objects.all()
    context = {'appointments': appointments}
    return render(request, 'list_appointments.html', context)

# administration/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Department
from .forms import DepartmentForm
from django.contrib import messages

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'department_form.html', {'form': form})

def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully.')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'department_form.html', {'form': form})

def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully.')
        return redirect('department_list')
    return render(request, 'department_confirm_delete.html', {'department': department})
# administration/views.py

from django.shortcuts import render, redirect
from .models import Department, Doctor
from .forms import DoctorForm
from django.contrib import messages

def add_doctor(request, department_id):
    department = Department.objects.get(pk=department_id)

    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.department = department
            doctor.save()
            messages.success(request, 'Doctor added successfully.')
            return redirect('department_list')
    else:
        form = DoctorForm()
    
    context = {
        'form': form,
        'department': department,
    }
    return render(request, 'add_doctor.html', context)
# administration/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('user_profile')  # Replace 'user_profile' with the URL for the user's profile page
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    return render(request, 'user_login.html', {'form': form})

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user_registration.html', {'form': form})
