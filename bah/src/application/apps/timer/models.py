from django.db import models

class Upload(models.Model):
    file_name = models.CharField(max_length=255, default='')
    file_type = models.CharField(max_length=50, default='')
    load_type = models.CharField(max_length=50, default='')
    file_size = models.BigIntegerField(default=0)
    header = models.CharField(max_length=255, default='')
    create_date = models.CharField(max_length=255, default='')
    start_time = models.FloatField(default=0.0)
    elapsed_time = models.FloatField(default=0.0)
    memory_consumed = models.FloatField(default=0.0)
    file_obj_type = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name    
