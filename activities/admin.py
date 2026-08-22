
from django.contrib import admin
from django.utils.html import format_html

from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "image_thumb",
        "name",
        "city",
        "activity_type",
        "duration",
        "estimated_cost",
    )
    list_filter = ("activity_type", "city__country", "city")
    search_fields = (
        "name",
        "description",
        "city__name",
        "city__country",
    )
    autocomplete_fields = ("city",)
    ordering = ("city__name", "name")
    list_per_page = 30
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Activity", {
            "fields": ("city", "name", "description", "activity_type")
        }),
        ("Planning", {
            "fields": ("duration", "estimated_cost")
        }),
        ("Imagery", {
            "fields": ("image", "external_image_url", "image_preview"),
            "description": "Upload a local image or provide a trusted image/CDN URL."
        }),
    )

    @admin.display(description="Preview")
    def image_thumb(self, obj):
        url = obj.image.url if obj.image else obj.external_image_url
        if not url:
            return "—"
        return format_html(
            '<img src="{}" style="width:48px;height:36px;object-fit:cover;border-radius:7px;" />',
            url,
        )

    @admin.display(description="Image preview")
    def image_preview(self, obj):
        url = obj.image.url if obj.image else obj.external_image_url
        if not url:
            return "No image selected."
        return format_html(
            '<img src="{}" style="max-width:420px;max-height:260px;object-fit:cover;border-radius:10px;border:1px solid #ddd;" />',
            url,
        )
