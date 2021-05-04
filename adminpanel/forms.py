from datetime import datetime, time, date, timedelta
from django import forms
from .models import *
import datetime
from account.models import User
from ckeditor.widgets import CKEditorWidget


min_date = date.today() - timedelta(50*365)
today = date.today() - timedelta(18*365)


class Gallery_Form(forms.ModelForm):
    date = forms.DateField(widget=forms.DateTimeInput(format=('%Y-%m-%d'), attrs={
                           'class': 'form-control datepicker', 'max': date.today(), 'value': today,  'type': 'date'}))

    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Title of the Event"}))

    description = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Description of the event"}))

    class Meta:
        model = Gallery
        fields = '__all__'
        exclude = ['photo']


class About_Us_Form(forms.ModelForm):

    highlight_line = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Highlight Line"}))

    vision = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Vision"}))
    mission = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Mission"}))

    aim = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Aim"}))



    class Meta:
        model = About_Us
        fields = '__all__'


class Blog_Form(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Title of the Blog"}))
    date = forms.DateField(widget=forms.DateTimeInput(format=('%Y-%m-%d'), attrs={
                           'class': 'form-control datepicker', 'max': date.today(), 'value': today,  'type': 'date'}))
    
    highlight_line = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Highlight Text"}))

    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['user']


class Banner_Form(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control'}),required=True)
    class Meta:
        model = Banner
        fields = '__all__'



class ContentMainForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Title"}))
    position = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Position",'type':'number'}))

    class Meta:
        model = MainPage
        fields = '__all__'
        exclude = ['sub']
class ContentSubForm(forms.ModelForm):
    
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Title"}))
    position = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Highlight Text",'type':'number'}))
    class Meta:
        model = SubPage
        fields = '__all__'
      