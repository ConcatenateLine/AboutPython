from django.db import models

# Create your models here.
class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

