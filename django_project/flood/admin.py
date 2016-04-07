from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


# Register your models here.
from .models import Photo, RainLevel

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('date_taken', 'locality', 'score')
    list_filter = (PhotoListFilter)

class PhotoListFilter(SimpleListFilter):

    title = _('Negatively Rated')
    parameter_name = 'score'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('negative', _('negative')),
            ('positive', _('postive')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'negative':
            return Photo.objects.filter(score__lt=0)
        if self.value() == 'postive':
            return Photo.objects.filter(score__gt=0)



admin.site.register(Photo, PhotoAdmin)
admin.site.register(RainLevel)