from django.db import models

UPLOAD_CHOICES = (
    ('DIRECTORY', 'Upload to Current Directory'),
    ('SQLITE', 'Upload to SQLite'),
    ('MONGO', 'Upload to MongoDB'),
)

class Upload(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField()
    choice = models.CharField(max_length=50, choices=UPLOAD_CHOICES)
