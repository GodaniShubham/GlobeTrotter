from django.db import models
from django.contrib.auth.models import User
from core.models import AuditModel

class City(AuditModel):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=150)
    region = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='cities/', null=True, blank=True)
    cost_index = models.PositiveIntegerField(default=50, help_text="0-100 scale of how expensive it is")
    popularity = models.PositiveIntegerField(default=50, help_text="0-100 scale of popularity")

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.country}"

class SavedDestination(AuditModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_destinations')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='saved_by')

    class Meta:
        unique_together = ('user', 'city')

    def __str__(self):
        return f"{self.user.username} saved {self.city.name}"
