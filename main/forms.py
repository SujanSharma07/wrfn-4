from datetime import datetime, time, date, timedelta
from django import forms
from .models import *
import datetime
from account.models import User
from django_countries.data import COUNTRIES
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

min_date = date.today() 
today = date.today() 


class Personal_Info_Form(forms.ModelForm):

    birth_date = forms.DateField(widget=forms.DateTimeInput(format=('%Y-%m-%d'), attrs={'class': 'form-control datepicker', 'max': today, 'value': today,  'type': 'date'}),
                                 )
    facebook = forms.CharField(widget=forms.URLInput(
        attrs={'class': 'form-control'}), required=False)
    insta = forms.CharField(widget=forms.URLInput(
        attrs={'class': 'form-control'}), required=False, label='Instagram')
    twitter = forms.CharField(widget=forms.URLInput(
        attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Personal_Info
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control custom-select custom-select-lg mb-3'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),

            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'tag_line':forms.TextInput(attrs={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserUpdateForm(forms.ModelForm):
    country = forms.ChoiceField(choices=sorted(COUNTRIES.items()))
    country.widget.attrs.update(
        {'class': 'form-control'})

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Enter Your First Name Here"}))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Enter Your Last Name Here"}))

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Enter Your Username Here", 'type': 'email'}))
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='AD', attrs={
        'class': 'form-control', 'placeholder': "Phone Number", 'type': 'number'}))

    class Meta:
        model = User
        fields = ['country', 'first_name', 'last_name', "username", "phone"]
        exclude = ['is_client', 'is_modrator', 'is_photographer',
                   'is_admin', 'password2', 'password1']


class Document_Form(forms.ModelForm):

    id_front = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control documents_', 'onchange': "readURL(this);", 'placeholder': "Front Side of Document"}))
    id_back = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control documents_', 'onchange': "readURL1(this);", 'placeholder': "Back Side of Document"}))
    profile = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control documents_', 'onchange': "readURL2(this);", 'placeholder': "Lates Profile"}))

    class Meta:
        model = Documents
        fields = '__all__'
        exclude = ['user']


class Skills_Form(forms.ModelForm):
    area = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Area of Expertise"}),required=False)

    experience = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': "Experience"}),required=False)

    hard_skills = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Hard Skills"}),required=False)
    soft_skills = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Soft Skills"}),required=False)

    interests = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Your Interest"}),required=False)

    class Meta:
        model = Skills
        fields = '__all__'
        exclude = ['user']
