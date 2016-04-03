from django.contrib import admin

# Register your models here.
from .models import Photo, RainLevel
admin.site.register(Photo)
admin.site.register(RainLevel)