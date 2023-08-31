from .models import *  
from django import forms      



class AddPatientForm(forms.ModelForm):
    # Basic Information
    name = forms.CharField(label="Name")
    address = forms.CharField(label="Address", widget=forms.Textarea)
    specialities = forms.ModelMultipleChoiceField(label="Select Specialities", queryset=Speciality.objects.all(), widget=forms.SelectMultiple())
    branch = forms.ModelChoiceField(label="Select Location", queryset=Branch.objects.all())
    phone = forms.CharField(label="Phone Number")
    date_of_birth = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, widget=forms.RadioSelect)

    # Medical Information
    height = forms.DecimalField(label="Height (cm)", required=False)
    weight = forms.DecimalField(label="Weight (kg)", required=False)
    blood_group = forms.ChoiceField(label="Blood Group", choices=BLOOD_GROUP_CHOICES, required=False)
    notes = forms.CharField(label="Notes", widget=forms.Textarea, required=False)
    profile_photo = forms.ImageField(label="Upload Photo", required=False)

    # Create Login
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Set Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

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
        if commit:
            patient.set_password(self.cleaned_data["password"])  
            patient.save()
        patient.specialities.set(self.cleaned_data['specialities'])
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
            queryset = queryset.filter(user__first_name__icontains=name) | queryset.filter(user__last_name__icontains=name)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        if gender:
            queryset = queryset.filter(gender=gender)
        if location:
            queryset = queryset.filter(location=location)
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
