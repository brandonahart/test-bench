from django.db import models
from django.utils import timezone


class Project(models.Model):
    customer_name = models.CharField(max_length=50, null=True, blank=True)
    project_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
    #initial mapping field

    def __str__(self):
        return self.customer_name


# Create your models here.
class DataFile(models.Model):
    STATUS_CHOICE = (
        ('new', 'NEW'),
        ('mapped', 'MAPPED'),
        ('del', 'DEL'),
        ('valid', 'VALID')
    )

    file = models.FileField(upload_to='./static')
    file_name = models.CharField(max_length=50, null=True, blank=True)
    file_type = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    project_fk = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='datafiles', null=True, blank=True)
    year_quarter = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=50, null=True, blank=True)  
    description = models.CharField(max_length=50, null=True, blank=True)
    #s3_key = models.CharField(max_length=50, null=True, blank=True)
    #created_by_fk =
    # #record_cnt = models.IntegerField(default=0)
    file_mappings = models.TextField(blank=True)

    def __str__(self):
        return self.description


