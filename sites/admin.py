from django.contrib import admin

from sites.models import Visit


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['domain', 'datetime']
    search_fields = ['domain', 'datetime']
