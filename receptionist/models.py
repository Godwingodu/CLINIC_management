from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.apps import apps  # For deferred model import
from django.contrib.auth.hashers import make_password, check_password

from clinic_app.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from django.conf import settings

TWILIO_ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
from django.contrib.auth import get_user_model

User = get_user_model()



import logging

# Constants
PENDING = 'Pending'
ACCEPTED = 'Accepted'
REJECTED = 'Rejected'
COMPLETED = 'Completed'
CANCELLED = 'Cancelled'

# Initialize logger
logger = logging.getLogger(__name__)

# Create your models here.


class Branch(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    


    
#patients model

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    




class Patient(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    specialities = models.ManyToManyField('Speciality')
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # Medical Information
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='receptionist/patients/', default='path/to/default/image.jpg')
    
    # Login Information
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    
    # Timestamp of when the patient is added
    date_added = models.DateTimeField(auto_now_add=True)
    
    # Suggestion: Adding a human-readable unique patient ID 
    patient_id = models.CharField(max_length=10, unique=True)

    # Tags for the patient
    tags = models.ManyToManyField(Tag, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password if it's a new object.
            self.password = make_password(self.password)
        super(Patient, self).save(*args, **kwargs)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.name

    
 


#PHYSIOTHERAPIST MODEL


# Speciality Model
class Speciality(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class WorkingDay(models.Model):
    day_name = models.CharField(max_length=20)
    weekday_number = models.IntegerField()  # <-- Add this line

    def __str__(self):
        return self.day_name

# Time Slot Model
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

# Therapist Model
class Therapist(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    qualification = models.CharField(max_length=200)  # Added Qualification
    specialities = models.ManyToManyField(Speciality)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    appointment_interval = models.PositiveIntegerField()  # Changed name to appointment_interval
    working_days = models.ManyToManyField(WorkingDay, through='TherapistWorkingDay')  # Through an intermediary model
    is_active = models.BooleanField(default=True)
    profile_photo = models.ImageField(upload_to='receptionist/therapists/', blank=True, null=True)

    def __str__(self):
        return self.name

# Therapist Working Day Through Model
class TherapistWorkingDay(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    working_day = models.ForeignKey(WorkingDay, on_delete=models.CASCADE)
    time_slots = models.ManyToManyField(TimeSlot)

# Therapist Login Model
class TherapistLogin(models.Model):
    therapist = models.OneToOneField(Therapist, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='receptionist/therapists/logins/', blank=True, null=True)

    def __str__(self):
        return f"Login for {self.therapist.name}"
    

   

    

#APPOINTMENT MODEL



APPOINTMENT_STATUS = [
    (PENDING, 'Pending'),
    (ACCEPTED, 'Accepted'),
    (REJECTED, 'Rejected'),
    (COMPLETED, 'Completed'),
    (CANCELLED, 'Cancelled'),
]

def send_sms(message, to):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(body=message, from_=settings.TWILIO_PHONE_NUMBER, to=to)
    except TwilioRestException as e:
        logger.error(f"An error occurred while sending the SMS: {str(e)}")

class Appointment(models.Model):
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='appointments')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, related_name='appointments')
    appointment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default=PENDING)
    invoice = models.OneToOneField('Invoice', null=True, blank=True, on_delete=models.SET_NULL, related_name='related_appointment')

    class Meta:
        unique_together = ('therapist', 'time_slot', 'appointment_date')
        ordering = ['appointment_date', 'time_slot']

    def __str__(self):
        return f"{self.patient.user.first_name} appointment with {self.therapist.name} on {self.appointment_date}"



    # Check if the appointment is for today
    def is_today(self):
        return timezone.now().date() == self.appointment_date

    # Custom validations
    def clean(self):
        super().clean()
        working_days = self.therapist.working_days.all()
        if self.appointment_date.weekday() not in [d.weekday_number for d in working_days]:
            raise ValidationError(_('The selected date is not a working day for this therapist.'))

        overlapping_appointments = Appointment.objects.filter(
            therapist=self.therapist,
            appointment_date=self.appointment_date,
            time_slot=self.time_slot,
            status__in=[PENDING, ACCEPTED]
        ).exclude(id=self.id)
        if overlapping_appointments.exists():
            raise ValidationError(_('The selected time slot is already booked.'))

    # Save method
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # String representation of the model
    def __str__(self):
        return f"{self.patient.user.first_name} appointment with {self.therapist.name} on {self.appointment_date}"

    # Check if the appointment is upcoming
    @property
    def is_upcoming(self):
        return timezone.now().date() < self.appointment_date

    # Check if the appointment is past due
    @property
    def is_past_due(self):
        return timezone.now().date() > self.appointment_date

# Signal to send SMS when appointment is created or updated
@receiver(post_save, sender=Appointment)
def appointment_created_or_updated(sender, instance, created, **kwargs):
    if created:
        doctor_message = f"A new appointment {instance.id} is scheduled for {instance.appointment_date} at {instance.time_slot.start_time} with the patient {instance.patient.user.first_name}. Thank you. Meditrac Team"
        patient_message = f"Your appointment {instance.id} with {instance.therapist.name} is scheduled for {instance.appointment_date} at {instance.time_slot.start_time}. Thank you. Meditrac Team"
    else:
        doctor_message = f"Appointment {instance.id} with {instance.therapist.name} has been updated to {instance.appointment_date} at {instance.time_slot.start_time}."
        patient_message = f"Your appointment {instance.id} with {instance.therapist.name} has been updated to {instance.appointment_date} at {instance.time_slot.start_time}."

    try:
        send_sms(doctor_message, instance.therapist.phone)
        send_sms(patient_message, instance.patient.phone)
    except TwilioRestException as e:
        logger.error(f"An error occurred while sending the SMS: {str(e)}")

# Signal to send SMS when appointment is cancelled
@receiver(pre_delete, sender=Appointment)
def appointment_cancelled(sender, instance, **kwargs):
    message = f"Your appointment with {instance.therapist.name} on {instance.appointment_date} has been cancelled."
    send_sms(message, instance.patient.phone)



class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    medication = models.TextField()
    dosage = models.TextField()
    frequency = models.CharField(max_length=100)
    additional_notes = models.TextField(blank=True, null=True)
    date_issued = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.user.first_name} from {self.therapist.name}"
        







#accounts model
class Invoice(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]
    
    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash Payment'),
        ('card', 'Card Payment'),
        ('net', 'Net Banking'),
    ]
    
    invoice_number = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, related_name='invoices', on_delete=models.CASCADE)
    invoice_date = models.DateField(default=timezone.now)
    appointment = models.OneToOneField('Appointment', null=True, blank=True, on_delete=models.SET_NULL, related_name='related_invoice')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES)
    therapist = models.ForeignKey(Therapist, related_name='invoices', on_delete=models.SET_NULL, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def recalculate_totals(self):
        self.subtotal = sum(item.amount for item in self.invoice_items.all())
        self.tax = self.subtotal * 0.10  # Assuming a 10% tax rate for now
        self.total_amount = self.subtotal + self.tax

    def save(self, *args, **kwargs):
        self.recalculate_totals()
        
        if not self.invoice_number:
            current_date = timezone.now().strftime('%Y%m%d')
            last_invoice = Invoice.objects.filter(invoice_number__startswith=current_date).order_by('-invoice_number').first()
            
            if last_invoice:
                last_id = int(last_invoice.invoice_number.split('-')[1])
                self.invoice_number = '{}-{:04d}'.format(current_date, last_id + 1)
            else:
                self.invoice_number = '{}-{:04d}'.format(current_date, 1)
                
        super().save(*args, **kwargs)


    def __str__(self):
      return str(self.invoice_number)


# The rest of your models (InvoiceItem, ExportFormat, ExportedInvoice) remain unchanged


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.item_name

class ExportFormat(models.Model):
    format_name = models.CharField(max_length=50)

    def __str__(self):
        return self.format_name


class ExportedInvoice(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    export_format = models.ForeignKey(ExportFormat, on_delete=models.SET_NULL, null=True)
    exported_date = models.DateField(auto_now_add=True)
    file_path = models.FileField(upload_to='exported_invoices/')

    def __str__(self):
        return f"Exported {self.invoice}"

