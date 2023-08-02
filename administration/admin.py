from django.contrib import admin

# Register your models here.
from .models import Department,Doctor,Patient,Appointment,SuperAdmin,Admin,TimeSlot
admin.site.register(Doctor)
admin.site.register(Department)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(SuperAdmin)
admin.site.register(TimeSlot)


