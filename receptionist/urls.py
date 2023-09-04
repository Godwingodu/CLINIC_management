from django.urls import path
from . import views  # Import the views module, rather than all individual views

urlpatterns = [
    # Receptionist Dashboard
    path('receptionist_dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),

    # Patient URLs
    path('patient/add/', views.add_new_patient, name='add_new_patient'),
    path('patient/list/', views.patient_list, name='patient_list'),
    path('patient/profile/<int:pk>/', views.PatientProfileView.as_view(), name='patient_profile'),
    path('patient/update/<int:pk>/', views.update_patient, name='update_patient'),
    path('patient/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('path_to_get_patient_details/<int:patient_id>/', views.get_patient_details, name='get_patient_details'),

    # Therapist URLs
    path('therapist/add/', views.add_new_therapist, name='add_new_therapist'),
    path('therapist/list/', views.list_therapists, name='list_therapists'),
    path('therapist/profile/<int:therapist_id>/', views.get_therapist_profile, name='get_therapist_profile'),

    # Speciality URLs
    path('speciality/add/', views.add_new_speciality, name='add_new_speciality'),

    # Prescription URLs
    path('prescription/add/<int:appointment_id>/', views.add_prescription, name='add_prescription'),
 # Appointment URLs
    path('appointment/<int:appointment_id>/', views.get_appointment_detail, name='get_appointment_detail'),
    path('appointment/schedule/', views.schedule_appointment, name='schedule_appointment'),
    path('appointment/schedule/<int:patient_id>/', views.schedule_appointment, name='schedule_appointment_with_patient'),
    path('appointment/list/', views.list_appointments, name='list_appointments'),
    path('appointment/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('appointment/update/<int:appointment_id>/', views.update_appointment, name='reschedule_appointment'),  # New line for update
    # Calendar URL
    path('calendar/', views.calendar_view, name='calendar_view'),
    # Invoice URLs
    path('invoice/create/', views.create_invoice, name='create_invoice'),
    path('invoice/create/<int:appointment_id>/', views.create_invoice, name='create_invoice_with_appointment'),
    path('invoice/list/', views.invoice_list, name='invoice_list'),
    path('invoice/update_status/<int:invoice_id>/', views.update_invoice_status, name='update_invoice_status'),
    path('invoice/export/', views.export_invoices, name='export_invoices'),
    path('invoice/paid/', views.paid_invoices, name='paid_invoices'),
    path('invoice/unpaid/', views.unpaid_invoices, name='unpaid_invoices'),
    path('invoice/view_paid/<int:invoice_id>/', views.view_paid_invoice, name='view_paid_invoice'),
    path('invoice/view_unpaid/<int:invoice_id>/', views.view_unpaid_invoice, name='view_unpaid_invoice'),

    # Search URL
    path('search_patients/', views.search_patients, name='search_patients'),


 
]
