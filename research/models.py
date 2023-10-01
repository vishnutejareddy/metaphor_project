from django.db import models

# Create your models here.
class Paper(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    summary = models.TextField()
    link = models.URLField()