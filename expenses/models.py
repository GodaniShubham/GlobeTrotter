from django.db import models
from core.models import AuditModel
from trips.models import Trip, TripStop

class Expense(AuditModel):
    CATEGORY_CHOICES = [
        ('Transport', 'Transport'),
        ('Accommodation', 'Accommodation'),
        ('Activities', 'Activities'),
        ('Meals', 'Meals'),
        ('Other', 'Other'),
    ]

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='expenses')
    trip_stop = models.ForeignKey(TripStop, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category}: {self.amount} {self.currency} for {self.trip.name}"
