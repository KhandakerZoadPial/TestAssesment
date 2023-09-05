from django.db import models

# Create your models here.
class JsonFiles(models.Model):
    file = models.FileField(upload_to='json_files/')