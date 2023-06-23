"""

Description: Module handles the fields that the form uses for the view function

"""
from django import forms
from .models import Upload

def validate_file_extension(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV file is accepted")

class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_extension])
    location = forms.ChoiceField(choices=(('DIRECTORY', 'Upload to Current Directory'), ('SQLITE', 'Upload to SQLite'), ('MONGO', 'Upload to MongoDB'), ('S3', 'Upload to Amazon S3')))

class UploadMultiFileForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}))
