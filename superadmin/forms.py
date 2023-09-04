from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Appointment


class BranchCreationForm(forms.Form):
    name = forms.CharField(max_length=155, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}))
    phone = PhoneNumberField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}))
    status = forms.BooleanField()


class BranchAdminCreationForm(forms.Form):
    name = forms.CharField(max_length=155, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    phone = PhoneNumberField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}))
    branch = forms.CharField(max_length=155, widget=forms.TextInput(attrs={'placeholder': 'Select Branch', 'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Set Password', 'class': 'form-control password-field', 'autocomplete': 'off'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control password-field', 'autocomplete': 'off'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")


class ReceptionistCreationForm(forms.Form):
    name = forms.CharField(max_length=155, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    phone = PhoneNumberField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}))
    branch = forms.CharField(max_length=155, widget=forms.TextInput(attrs={'placeholder': 'Select Branch', 'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Set Password', 'class': 'form-control password-field', 'autocomplete': 'off'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control password-field', 'autocomplete': 'off'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match.")


class TherapistCreationForm(forms.Form):
    GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ]

    MINUTE_CHOICES = [(str(i), str(i)) for i in range(1, 61)]

    name = forms.CharField(max_length=155, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}))
    # slot = forms.ModelChoiceField(queryset=Appointment.objects.all(), empty_label="Specialities",
    #                                     widget=forms.Select(attrs={'class': 'form-select'}))
    phone = PhoneNumberField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    gender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'gender-radio'}), choices=GENDER_CHOICES)
    minute = forms.ChoiceField(choices=MINUTE_CHOICES, widget=forms.Select)


class SpecialityCreationForm(forms.Form):
    name = forms.CharField(max_length=155, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control'}))