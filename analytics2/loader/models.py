from django.db import models
from django.utils import timezone


# DataFiles will have a foreign key for the possible quarter they belong to 
# and then the quarter model will have a foreign key for the project id
# they belong to

class Project(models.Model):
    customer_name = models.CharField(max_length=50, null=True, blank=True)
    project_id = models.CharField(max_length=50, null=True, blank=True)
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

    file_name = models.CharField(max_length=50, null=True, blank=True)
    file_type = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    project_fk = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='datafiles', null=True, blank=True)
    year_quarter = models.CharField(max_length=50, null=True, blank=True)
    #s3_key = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    #created_by_fk =
    size = models.CharField(max_length=50, null=True, blank=True)
    #record_cnt = models.IntegerField(default=0)'''
    description = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.description


