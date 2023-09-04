from django.contrib import admin

from .models import Invoices, Appointment

# Register your models here.


admin.site.register(Invoices)
admin.site.register(Appointment)