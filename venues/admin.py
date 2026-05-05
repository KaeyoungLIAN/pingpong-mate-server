from django.contrib import admin
from .models import Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'district', 'phone', 'status', 'created_at']
    list_filter = ['status', 'district']
    search_fields = ['name', 'address']
