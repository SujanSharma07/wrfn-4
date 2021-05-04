from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from django.conf import settings
#from phone_field import PhoneField
from django_countries.data import COUNTRIES

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class UserForm(UserCreationForm):
    country = forms.ChoiceField(choices=sorted(COUNTRIES.items()))
    country.widget.attrs.update(
        {'class': 'form-control'})

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Enter Your First Name Here"}))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Enter Your Last Name Here"}))

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Enter Your Email Here", 'type': 'email'}), label='Email')
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='NP', attrs={
                             'class': 'form-control', 'placeholder': "Phone Number", 'type': 'number'}))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password'}
    ), label='Password', required=True, max_length=50)

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter password'}
    ), label='Confirm Password', required=True, max_length=50)

    class Meta:
        model = User
        fields = ['country', 'first_name', 'last_name', "username", "phone", "password1", "password2",
                  ]
        exclude = ['membership']


class SigninForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ["username", "password1"]


class PasswordReset(PasswordResetForm):
    class Meta():
        model = User
        fields = "__all__"
