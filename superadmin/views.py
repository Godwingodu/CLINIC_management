from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.core.paginator import Paginator

from datetime import date
from django.utils.dateparse import parse_date

from .models import Appointment


from .forms import (
    BranchCreationForm,
    BranchAdminCreationForm,
    ReceptionistCreationForm,
    TherapistCreationForm,
    SpecialityCreationForm
    )

# Views


class SuperadminOverview(TemplateView):
    template_name = 'superadmin/overview/overview.html'


# super admin (branch management)

class BranchList(TemplateView):
    template_name = 'superadmin/branches/branch_list.html'

class AddNewBranch(FormView):
    form_class = BranchCreationForm
    template_name = 'superadmin/branches/add_new_branch.html'


# super admin (branch admins management)

class BranchAdminsList(TemplateView):
    template_name = 'superadmin/branch_admin/branch_admins_list.html'


class AddNewAdmin(FormView):
    form_class = BranchAdminCreationForm
    template_name = 'superadmin/branch_admin/add_new_admin.html'


# super admin (receptionist management)

class ReceptionistList(TemplateView):
    template_name = 'superadmin/receptionist/receptionist_list.html'


class AddNewReceptionist(FormView):
    form_class = ReceptionistCreationForm
    template_name = 'superadmin/receptionist/add_new_receptionist.html'


# superadmin (Therapist management)


class TherapistList(TemplateView):
    template_name = 'superadmin/therapist/therapist_list.html'


class AddNewTherapist(FormView):
    form_class = TherapistCreationForm
    template_name = 'receptionist/therapist/add_new_therapist.html'


class AddNewSpeciality(FormView):
    form_class = SpecialityCreationForm
    template_name = 'superadmin/therapist/add_new_speciality.html'


class NewRequestsView(TemplateView):
    template_name = 'superadmin/therapist/new_requests.html'


# superadmin(patient management)

class PatientsListView(TemplateView):
    template_name = 'superadmin/patients/patients_list.html'


# superadmin(appointment management)

def superadmin_appointments_filter_view(request):
    today = date.today().isoformat() 
    filter_param = request.GET.get('filter')

    if filter_param == 'today':
        appointments = Appointment.objects.filter(date=today)
    elif filter_param in ['upcoming', 'completed', 'cancelled']:
        appointments = Appointment.objects.filter(status=filter_param)
    else:
        appointments = Appointment.objects.filter(date=today)  # Default to today


    page = Paginator(appointments, 8)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    appointments = page.object_list
    continuous_number = (page.number - 1) * page.paginator.per_page + 1

    for entry in appointments:
        entry.continuous_number = continuous_number
        continuous_number += 1

    context = {
        'page': page,
        'filter': filter_param
        }
    return render(request, 'superadmin/appointment/appointment_list.html', context)