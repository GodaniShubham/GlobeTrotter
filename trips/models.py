from django.db import models
from django.contrib.auth.models import User
from core.models import AuditModel
from django.utils.text import slugify
import uuid

class Trip(AuditModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    cover_image = models.ImageField(upload_to='trip_covers/', null=True, blank=True)
    is_public = models.BooleanField(default=False)
    public_slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.public_slug:
            # Generate a unique slug
            base_slug = slugify(self.name)
            unique_id = str(uuid.uuid4())[:8]
            self.public_slug = f"{base_slug}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"

class TripStop(AuditModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='stops')
    city = models.ForeignKey('destinations.City', on_delete=models.CASCADE, related_name='trip_stops')
    arrival_date = models.DateField()
    departure_date = models.DateField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Stop {self.order} for {self.trip.name}"

class ItineraryActivity(AuditModel):
    trip_stop = models.ForeignKey(TripStop, on_delete=models.CASCADE, related_name='itinerary_activities')
    activity = models.ForeignKey('activities.Activity', on_delete=models.CASCADE, related_name='planned_instances')
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    custom_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['date', 'start_time', 'order']
        verbose_name_plural = "Itinerary Activities"

    def __str__(self):
        return f"{self.activity.name} on {self.date}"
