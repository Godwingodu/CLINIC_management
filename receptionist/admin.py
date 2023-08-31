from django.contrib import admin
from .models import (
    Branch,
    Tag,
    Patient,
    Speciality,
    WorkingDay,
    TimeSlot,
    Therapist,
    TherapistWorkingDay,
    TherapistLogin,
    Appointment,
    Prescription,
    Invoice,
    InvoiceItem,
    ExportFormat,
    ExportedInvoice
)

# Inline models for ManyToMany relationships
class SpecialityInline(admin.TabularInline):
    model = Therapist.specialities.through

class WorkingDayInline(admin.TabularInline):
    model = Therapist.working_days.through

class TagInline(admin.TabularInline):
    model = Patient.tags.through

# Admin interfaces for models
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'address', 'phone_number', 'is_active']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_of_birth', 'gender']
    inlines = [TagInline]

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    pass

@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    pass

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    pass

@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_of_birth', 'gender']
    inlines = [SpecialityInline, WorkingDayInline]

@admin.register(TherapistWorkingDay)
class TherapistWorkingDayAdmin(admin.ModelAdmin):
    pass

@admin.register(TherapistLogin)
class TherapistLoginAdmin(admin.ModelAdmin):
    pass

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'therapist', 'time_slot', 'appointment_date', 'status']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'therapist', 'date_issued']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'patient', 'invoice_date', 'status', 'payment_mode', 'therapist']

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    pass

@admin.register(ExportFormat)
class ExportFormatAdmin(admin.ModelAdmin):
    pass

@admin.register(ExportedInvoice)
class ExportedInvoiceAdmin(admin.ModelAdmin):
    pass
