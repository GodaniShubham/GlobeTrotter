from django.db import models

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_ip = models.GenericIPAddressField(null=True, blank=True, help_text="IP address of the creator")
    created_location = models.CharField(max_length=255, null=True, blank=True, help_text="Approximate location of the creator")

    class Meta:
        abstract = True
