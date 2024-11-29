from django import forms
from .models import UploadedFile  # Import the UploadedFile model

# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = UploadedFile  # Link the form to the UploadedFile model
#         fields = ['file']  # Only include the `file` field in the form
class FileUploadForm(forms.Form):
    file = forms.FileField(label='Upload Excel File')