from django.db import models

# Create your models here.
# administration/models.py

from django.contrib.auth.models import User

class SuperAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# administration/models.py


class Department(models.Model):
    name = models.CharField(max_length=100)

# class Doctor(models.Model):
#     name = models.CharField(max_length=100)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
#     qualification = models.CharField(max_length=200)

class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    place = models.CharField(max_length=100)

class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.CharField(max_length=10, choices=[
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ])

# administration/models.py

from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    qualification = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ])

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add related_name to avoid clashes with auth.User model
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email