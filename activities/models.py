from django.db import models
from core.models import AuditModel
from destinations.models import City

class Activity(AuditModel):
    ACTIVITY_TYPES = [
        ('Sightseeing', 'Sightseeing'),
        ('Food', 'Food'),
        ('Adventure', 'Adventure'),
        ('Museum', 'Museum'),
        ('Shopping', 'Shopping'),
        ('Nature', 'Nature'),
        ('Entertainment', 'Entertainment'),
        ('Nightlife', 'Nightlife'),
        ('Other', 'Other'),
    ]

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES, default='Sightseeing')
    duration = models.PositiveIntegerField(help_text="Estimated duration in minutes", default=60)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='activities/', null=True, blank=True)
    external_image_url = models.URLField(max_length=1000, blank=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} in {self.city.name}"
