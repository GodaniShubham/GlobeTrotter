from django.contrib import admin
from .models import Trip, TripStop, ItineraryActivity

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'start_date', 'end_date', 'is_public', 'created_ip', 'created_location')
    list_filter = ('is_public', 'start_date')
    search_fields = ('name', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at', 'created_ip', 'created_location', 'public_slug')

@admin.register(TripStop)
class TripStopAdmin(admin.ModelAdmin):
    list_display = ('trip', 'city', 'arrival_date', 'departure_date', 'order')
    list_filter = ('arrival_date',)
    readonly_fields = ('created_at', 'updated_at', 'created_ip', 'created_location')

@admin.register(ItineraryActivity)
class ItineraryActivityAdmin(admin.ModelAdmin):
    list_display = ('activity', 'trip_stop', 'date', 'start_time')
    list_filter = ('date',)
    search_fields = ('activity__name', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'created_ip', 'created_location')
