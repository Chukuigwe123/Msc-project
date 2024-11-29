from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # This allows file uploads and saves them in the `uploads/` folder.
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically records when the file is uploaded.

