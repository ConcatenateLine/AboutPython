import uuid
from django.db import models
from django.shortcuts import reverse

# Create your models here.
class CustomCalendar(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    objetives = models.ManyToManyField('Objetive', blank=True)
    themes = models.ManyToManyField('Theme', blank=True)

    def __str__(self):
        return self.name

class Objetive(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    calendar = models.ForeignKey('CustomCalendar', on_delete=models.CASCADE)
    themes = models.ManyToManyField('Theme', blank=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    @property
    def get_html_url(self):
        url = reverse('calendar:objective_edit', args=(self.uuid,))
        return f'<a href="{url}"> {self.title} </a>'

class Theme(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7)
    
    def __str__(self):
        return self.name    