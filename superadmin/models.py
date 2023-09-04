from django.db import models

# Create your models here.

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    name = models.CharField(max_length=155)
    doctor_name = models.CharField(max_length=155)
    patient_number = PhoneNumberField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')

    def __str__(self):
        return self.name


class Invoices(models.Model):
    patient_id = models.CharField(max_length=6)
    name = models.CharField(max_length=155)
    doctor_name = models.CharField(max_length=155)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.BooleanField(default=False)