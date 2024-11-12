from django.contrib.admin import register
from netbox.admin import admin_site
from .models import DHCPServer

from django.contrib.admin.options import ModelAdmin
@register(DHCPServer,site=admin_site)
class DHCPReservationAdmin(ModelAdmin):
    list_display = (
        'name',
        'api_token',
        'api_url',
    )
