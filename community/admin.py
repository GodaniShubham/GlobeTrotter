from django.contrib import admin

from .models import (
    CommunityLike,
    CommunityNotification,
    CommunityPost,
    CommunityReply,
    CommunityReplyLike,
    CommunityReport,
    CommunitySave,
)


@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "city", "is_published", "created_at")
    list_filter = ("category", "is_published", "comments_enabled")
    search_fields = ("title", "body", "author__username", "author__email", "city__name")
    list_select_related = ("author", "city")
    ordering = ("-created_at",)


@admin.register(CommunityReply)
class CommunityReplyAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "parent", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("body", "author__username", "post__title")


@admin.register(CommunityReport)
class CommunityReportAdmin(admin.ModelAdmin):
    list_display = ("post", "reporter", "reason", "status", "created_at")
    list_filter = ("reason", "status")
    search_fields = ("post__title", "reporter__username", "note")


@admin.register(CommunityNotification)
class CommunityNotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "actor", "kind", "is_read", "created_at")
    list_filter = ("kind", "is_read")
    search_fields = ("recipient__username", "actor__username", "message")


admin.site.register(CommunityLike)
admin.site.register(CommunityReplyLike)
admin.site.register(CommunitySave)
