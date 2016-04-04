from django.contrib import admin

# Register your models here.
from .models import Photo, RainLevel

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('date_taken', 'locality')
    list_filter = ('locality')

admin.site.register(Photo, PhotoAdmin)
admin.site.register(RainLevel)