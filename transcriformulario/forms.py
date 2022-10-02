from django import forms
from django.forms import ModelForm



class PostForm(forms.Form):
    enlace= forms.CharField(max_length=100)

class CanalForm(forms.Form):
    canal= forms.CharField(max_length=100)