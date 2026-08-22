from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('trip', 'category', 'amount', 'currency', 'trip_stop', 'created_at')
    list_filter = ('category', 'currency')
    search_fields = ('description', 'trip__name')
    readonly_fields = ('created_at', 'updated_at', 'created_ip', 'created_location')
