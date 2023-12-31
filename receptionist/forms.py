from .models import *  
from django import forms 
from django.contrib.auth.password_validation import validate_password  
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password, check_password
from .constants import STATUS_CHOICES,PAYMENT_MODE_CHOICES
from django.forms.widgets import CheckboxSelectMultiple
import datetime






from .models import Therapist, WorkingDay
from .widgets import CustomCheckboxSelectMultiple 

from receptionist.models import Invoice

    




class AddPatientForm(forms.ModelForm):
    # Basic Information
    name = forms.CharField(max_length=155, widget=forms.TextInput(
        attrs={'placeholder': 'Name', 'class': 'form-control'}))
    address = forms.CharField(label="Address", widget=forms.TextInput(
        attrs={'placeholder': 'Address', 'class': 'form-control'}))
    specialities = forms.ModelChoiceField(
        empty_label="Specialities", queryset=Speciality.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(), empty_label="Select Location", widget=forms.Select(attrs={'class': 'form-select'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'placeholder': 'Phone', 'class': 'form-control'}))
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date of Birth', 'id': 'dateOfBirthInput'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-radio'}))

    # Medical Information
    height = forms.DecimalField(required=False)
    weight = forms.DecimalField(label="Weight (kg)", required=False)
    blood_group = forms.ChoiceField(label="Blood Group", choices=BLOOD_GROUP_CHOICES, required=False)
    notes = forms.CharField(
        label="Notes", widget=forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Notes'}), required=False)
    profile_photo = forms.ImageField(label="Upload Photo", required=False)

    # Create Login
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(
        label="Set Password", widget=forms.PasswordInput(attrs={'placeholder': 'Set Password', 'class': 'form-control password-field', 'autocomplete': 'off'}))
    confirm_password = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control password-field', 'autocomplete': 'off'}))

    class Meta:
        model = Patient
        fields = [
            'name', 'address', 'specialities', 'branch', 'phone',
            'date_of_birth', 'gender', 'height', 'weight', 
            'blood_group', 'notes', 'profile_photo',
            'email', 'password', 'confirm_password'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password do not match"
            )

    def save(self, commit=True):
        patient = super(AddPatientForm, self).save(commit=False)
        patient.email = self.cleaned_data["email"]

        # Securely set the password
        password = self.cleaned_data["password"]
        patient.password = make_password(password)

        if commit:
            patient.save()
        # patient.specialities.set(self.cleaned_data["specialities"])
        return patient




class PatientFilterForm(forms.Form):
    name = forms.CharField(label='Patient Name', required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter patient name'}))
    phone = forms.CharField(label='Phone', required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
    gender = forms.ChoiceField(label='Gender', choices=[('', 'All')] + list(GENDER_CHOICES), required=False, widget=forms.Select(attrs={'class': 'custom-select'}))
    location = forms.ModelChoiceField(queryset=Branch.objects.all(), required=False)
    speciality = forms.ModelMultipleChoiceField(queryset=Speciality.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    date_added_from = forms.DateField(label='Date Added From', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    date_added_to = forms.DateField(label='Date Added To', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    order_by = forms.ChoiceField(label='Order By', choices=[('date_added', 'Date Added'), ('user__first_name', 'Name')], required=False, widget=forms.Select(attrs={'class': 'custom-select'}))
    def filter_queryset(self, queryset):
        name = self.cleaned_data.get('name')
        phone = self.cleaned_data.get('phone')
        gender = self.cleaned_data.get('gender')
        location = self.cleaned_data.get('location')
        speciality = self.cleaned_data.get('speciality')
        tags = self.cleaned_data.get('tags')
        date_added_from = self.cleaned_data.get('date_added_from')
        date_added_to = self.cleaned_data.get('date_added_to')
        order_by = self.cleaned_data.get('order_by')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        if gender:
            queryset = queryset.filter(gender=gender)
        if location:
            queryset = queryset.filter(branch=location)  # Assuming "branch" is equivalent to "location"
        if speciality:
            queryset = queryset.filter(specialities__in=speciality)
        if tags:
            queryset = queryset.filter(tags__in=tags)
        if date_added_from:
            queryset = queryset.filter(date_added__gte=date_added_from)
        if date_added_to:
            queryset = queryset.filter(date_added__lte=date_added_to)
        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset.distinct()  # We add .distinct() to ensure that we don't get duplicate entries





#physiotherapy forms


class AddTherapistForm(forms.ModelForm):

   
    email = forms.EmailField(
    label=_('Email'),
    widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #F2FEFB;'}),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Set Password'), 'style': 'background-color: #F2FEFB;'}),
        label=_('Set Password')
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Confirm Password'), 'style': 'background-color: #F2FEFB;'}),
        label=_('Confirm Password')
    )

    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Name'), 'style': 'background-color: #F2FEFB;'}),
    )

    qualification = forms.CharField(
        
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('qualification'), 'style': 'background-color: #F2FEFB;'}),
    )

    phone = forms.CharField(
        label=_('phone'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'background-color: #F2FEFB;'}),
    )

    address = forms.CharField(
        label=_('Address'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Address'), 'style': 'background-color: #F2FEFB;'}),
    )

    date_of_birth = forms.DateField(
        label=_('Date of Birth'),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'background-color: #F2FEFB;'}),
    )

    appointment_interval = forms.EmailField(
        label=_('appointment_interval'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 4rem; background-color: #F2FEFB;'}),
    )

    working_days = forms.ModelMultipleChoiceField(
        queryset=WorkingDay.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'style': 'background-color: #F2FEFB;'}),
        required=False,
        label=_('Working Days')
    )

    class Meta:
        model = Therapist
        fields = [
            'name',
            'address',
            'qualification',
            'specialities',
            'branch',
            'phone',
            'date_of_birth',
            'gender',
            'appointment_interval',
            'is_active',
            'profile_photo',
        ]
    widgets = {
        'branch': forms.Select(attrs={'class': 'form-control'}),
    }
    
    specialities = forms.ModelMultipleChoiceField(
        queryset=Speciality.objects.all(),
        widget=CheckboxSelectMultiple,  # Use the default CheckboxSelectMultiple widget
        required=False,
        label=_('Specialities')
    )

    gender = forms.ChoiceField(
        choices=Therapist.GENDER_CHOICES[0:],  # Exclude the empty option
        widget=forms.RadioSelect,
        label=_('Gender'),
    )

    def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.time_slot_fields = {}  # Initialize the new attribute
                for day in WorkingDay.objects.all():
                    field_name = f'time_slot_{day.day_name}'
                    label = _('Time Slot for ') + day.day_name
                    widget = forms.TextInput(attrs={'placeholder': _('e.g. 09:00-12:00, 14:00-18:00')})
                    self.fields[field_name] = forms.CharField(label=label, widget=widget, required=False)
                    self.time_slot_fields[day.day_name] = self.fields[field_name]  # Store the field in the new attribute
                

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords do not match."))
        validate_password(password2)
        return password2


class AddSpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = ['name', 'description']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
        }


class PrescriptionForm(forms.ModelForm):
    appointment = forms.ModelChoiceField(
        queryset=Appointment.objects.all(),
        widget=forms.Select(attrs={'class': 'selectpicker'}),
        label=_('Appointment'),
    )
    therapist = forms.ModelChoiceField(
        queryset=Therapist.objects.all(),
        widget=forms.Select(attrs={'class': 'selectpicker'}),
        label=_('Therapist'),
        disabled=True,  # disable this if it should be automatically filled
    )
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'selectpicker'}),
        label=_('Patient'),
        disabled=True,  # disable this if it should be automatically filled
    )
    medication = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label=_('Medication'),
    )
    dosage = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label=_('Dosage'),
    )
    frequency = forms.ChoiceField(
        choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')],
        widget=forms.RadioSelect,
        label=_('Frequency'),
    )
    additional_notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label=_('Additional Notes'),
    )

    class Meta:
        model = Prescription
        fields = [
            'appointment',
            'therapist',
            'patient',
            'medication',
            'dosage',
            'frequency',
            'additional_notes',
        ]

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validations here.
        # Example: Ensure the therapist and patient match the appointment
        therapist = cleaned_data.get('therapist')
        patient = cleaned_data.get('patient')
        appointment = cleaned_data.get('appointment')
        
        if appointment:
            if therapist and therapist != appointment.therapist:
                self.add_error('therapist', ValidationError(_('Therapist does not match with the appointment.')))
            
            if patient and patient != appointment.patient:
                self.add_error('patient', ValidationError(_('Patient does not match with the appointment.')))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamic initial data or queryset can be set here
        # self.fields['appointment'].queryset = ...


#Appointment form


class AppointmentForm(forms.ModelForm):
    speciality_filter = forms.ModelChoiceField(
        queryset=Speciality.objects.all(),
        empty_label="Department",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Appointment
        fields = ['patient', 'therapist', 'appointment_date', 'time_slot', 'status', 'remarks']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            # 'speciality': forms.Select(attrs={'class: form-select'}),
            'therapist': forms.Select(attrs={'class': 'form-select'}),
            'appointment_date': forms.DateInput(attrs={'class': 'form-control datepicker'}),
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-textarea'})
        }
        

        error_messages = {
            'appointment_date': {
                'required': 'Please select a valid date for the appointment.',
            },
            'time_slot': {
                'required': 'Please select a valid time slot.',
            },
        }




    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)

        self.fields['patient'].empty_label = "Select patient"
        self.fields['therapist'].empty_label = "Doctor"
        self.fields['time_slot'].empty_label = "Select time slot"
        self.fields['status'].empty_label = "Select status"

        if 'speciality_filter' in self.data:
            speciality_id = int(self.data.get('speciality_filter'))
            # Modify the queryset for 'therapist' field based on the selected speciality
            self.fields['therapist'].queryset = Therapist.objects.filter(speciality=speciality_id)




        if patient:
            self.fields['patient'].initial = patient
            self.fields['patient'].queryset = Patient.objects.filter(id=patient.id)
            self.fields['patient'].disabled = True

        if 'therapist' in self.data:
            try:
                therapist_id = int(self.data.get('therapist'))
                therapist = Therapist.objects.get(id=therapist_id)
                appointment_date = self.data.get('appointment_date')
                if appointment_date:
                    day_num = datetime.strptime(appointment_date, "%Y-%m-%d").weekday()
                    self.fields['time_slot'].queryset = TimeSlot.objects.filter(therapistworkingday__therapist=therapist, therapistworkingday__working_day__weekday_number=day_num)
            except (ValueError, Therapist.DoesNotExist):
                pass


#accounts form


# Form for searching invoices
class SearchInvoiceForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search invoices based on name, id, patient ID, therapist name, appointment date...'}),
    )

# Form for selecting export format
class ExportFormatForm(forms.Form):
    export_format = forms.ModelChoiceField(
        queryset=ExportFormat.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
    )
# Main Invoice Form
class InvoiceForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
    )
    invoice_date = forms.DateField(
        widget=forms.SelectDateWidget(),
    )
    appointment_date = forms.DateField(
        widget=forms.SelectDateWidget(),
    )
    appointment_time = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    payment_mode = forms.ChoiceField(choices=PAYMENT_MODE_CHOICES)

    therapist = forms.ModelChoiceField(
        queryset=Therapist.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2'}),
    )
    appointment = forms.ModelChoiceField(  # Add this field
        queryset=Appointment.objects.all(),
        required=False,  # Make it optional
        widget=forms.Select(attrs={'class': 'select2'}),
    )
    
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'patient', 'invoice_date', 'appointment_date', 'appointment_time', 'status', 'payment_mode', 'therapist', 'appointment']  # Add 'appointment' to fields list

    def clean(self):
        cleaned_data = super().clean()
        # Additional validations can be added here
        return cleaned_data

# Invoice Item Form
class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['item_name', 'description', 'amount']

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if data <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return data

# Formset for Invoice Items
InvoiceItemFormset = forms.inlineformset_factory(
    Invoice, InvoiceItem, 
    form=InvoiceItemForm, 
    extra=1, 
    can_delete=True
)
