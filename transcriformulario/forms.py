from django import forms
from django.forms import ModelForm



class PostForm(forms.Form):
    enlace= forms.CharField(max_length=100)
