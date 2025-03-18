import uuid
from django.db import models
from django.shortcuts import reverse

from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'

class PrivateMediaStorage(S3Boto3Storage):
    location = 'private_media'
    default_acl = 'private'
    file_overwrite = False

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
    format = models.CharField(max_length=100, default="Table")

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
    image = models.ForeignKey('ImageCF', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    @property
    def get_html_url(self):
        url = reverse('calendar:objective_edit', args=(self.uuid,))
        url_show = reverse('calendar:objective_show', args=(self.uuid,))
        
        if self.calendar.format == 'Table':
            return f'{self.title} <br/> <span id="openModal" class="open_modal relative bg-[var(--body-medium-color)] px-2 rounded cursor-pointer text-[var(--accent)] hover:text-[var(--button-custom-hover-bg)]" name="{url_show}">Show ⇰</span>'
        
        return f'{self.title} <br/> <span id="openModal" class="open_modal bg-[var(--body-quiet-color)] px-2 rounded cursor-pointer text-[var(--header-link-color)] hover:text-[var(--button-custom-hover-bg)]" name="{url_show}">Show ⇰</span>'

    @property
    def get_edit_html_url(self):
        url = reverse('calendar:objective_edit', args=(self.uuid,))

        return f'{url}'

class Theme(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7)
    
    def __str__(self):
        return self.name    

class ImageCF(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(storage=PrivateMediaStorage())
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def delete(self):
        self.image.delete(save=False)
        super().delete()
