"""

Description: Module handles the fields that the form uses for the view function

"""
from django import forms
from django.forms import ModelForm
from .models import Upload

class UploadForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Upload
        fields = ['title', 'file', 'choice']

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
