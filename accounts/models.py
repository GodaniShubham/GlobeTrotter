from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
        ('INR', 'Indian Rupee (₹)'),
        ('JPY', 'Japanese Yen (¥)'),
        ('AUD', 'Australian Dollar ($)'),
        ('CAD', 'Canadian Dollar ($)'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
