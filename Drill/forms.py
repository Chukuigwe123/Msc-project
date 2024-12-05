from django import forms
from .models import UploadedFile  


class FileUploadForm(forms.Form):
    file = forms.FileField(label='Upload Excel File')