from django.contrib import admin
from django.contrib.admin import SimpleListFilter
# Register your models here.
from .models import Photo, RainLevel

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('date_taken', 'locality')
    list_filter = ('locality',)

class PhotoListFilter(SimpleListFilter):
    print("")

admin.site.register(Photo, PhotoAdmin)
admin.site.register(RainLevel)