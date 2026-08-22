from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'activity_type', 'estimated_cost', 'duration')
    list_filter = ('activity_type', 'city')
    search_fields = ('name', 'city__name')
    readonly_fields = ('created_at', 'updated_at', 'created_ip', 'created_location')
