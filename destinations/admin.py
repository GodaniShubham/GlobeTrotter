
from django.contrib import admin
from django.utils.html import format_html

from .models import City, SavedDestination


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "image_thumb",
        "name",
        "country",
        "region",
        "cost_index",
        "popularity",
        "activity_total",
    )
    list_filter = ("country", "region")
    search_fields = ("name", "country", "region", "description")
    ordering = ("country", "name")
    list_per_page = 30
    readonly_fields = ("image_preview", "activity_total")
    fieldsets = (
        ("Destination", {
            "fields": ("name", "country", "region", "description")
        }),
        ("Discovery", {
            "fields": ("cost_index", "popularity")
        }),
        ("Imagery", {
            "fields": ("image", "external_image_url", "image_preview"),
            "description": "Upload a local image or provide a trusted image/CDN URL. Local upload takes priority."
        }),
        ("Catalog information", {
            "fields": ("activity_total",),
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

    @admin.display(description="Activities")
    def activity_total(self, obj):
        return obj.activities.count()


@admin.register(SavedDestination)
class SavedDestinationAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "created_at")
    search_fields = ("user__username", "user__email", "city__name", "city__country")
    list_select_related = ("user", "city")
    ordering = ("-created_at",)
