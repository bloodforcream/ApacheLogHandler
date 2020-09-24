from django.contrib import admin

from core.models import ApacheLog


class ApacheLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'log_date', 'http_method', 'uri', 'status_code', 'response_size')
    search_fields = ('ip_address', 'log_date', 'http_method', 'uri', 'status_code', 'response_size')

admin.site.register(ApacheLog, ApacheLogAdmin)
