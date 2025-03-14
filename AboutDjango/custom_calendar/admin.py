from django.contrib import admin
from .models import CustomCalendar, ImageCF, Objetive, Theme

# Register your models here.
admin.site.register(CustomCalendar)
admin.site.register(Objetive)
admin.site.register(Theme)
admin.site.register(ImageCF)
