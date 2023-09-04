from django.urls import path

from . import views


urlpatterns = [
    path('superadmin-overview/', views.SuperadminOverview.as_view(), name='superadmin_overview'),

    # branches
    path('branch-list/', views.BranchList.as_view(), name='branch_list'),
    path('add-new-branch/', views.AddNewBranch.as_view(), name='add_new_branch'),

    # branch admins
    path('branch-admins-list/', views.BranchAdminsList.as_view(), name='branch_admins_list'),
    path('add-new-admin/', views.AddNewAdmin.as_view(), name='add_new_admin'),

    # receptionist
    path('receptionist-list/', views.ReceptionistList.as_view(), name='receptionist_list'),
    path('add-new-receptionist/', views.AddNewReceptionist.as_view(), name='add_new_receptionist'),

    # therapist
    path('therapist-list/', views.TherapistList.as_view(), name='therapist_list'),
    path('add-new-therapist/', views.AddNewTherapist.as_view(), name='add_new_therapist'),
    path('add-new-speciality/', views.AddNewSpeciality.as_view(), name='add_new_speciality'),
    path('new-requests/', views.NewRequestsView.as_view(), name='new_requests'),

    # patients
    path("superadmin-patients-list/", views.PatientsListView.as_view(), name="superadmin_patients_list"),

    # appointments
    path("superadmin-appointments-list/", views.superadmin_appointments_filter_view, name="superadmin_appointments_list")

]