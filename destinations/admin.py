from django.contrib import admin
from .models import City, SavedDestination

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'cost_index', 'popularity')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    readonly_fields = ('created_at', 'updated_at', 'created_ip', 'created_location')

@admin.register(SavedDestination)
class SavedDestinationAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'created_at')
    search_fields = ('user__username', 'city__name')
    readonly_fields = ('created_at', 'updated_at', 'created_ip', 'created_location')
