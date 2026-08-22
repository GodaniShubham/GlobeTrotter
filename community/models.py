from django.contrib.auth.models import User
from django.db import models
from core.models import AuditModel


class CommunityPost(AuditModel):
    CATEGORY_CHOICES = [
        ("question", "Question"),
        ("destination", "Destination"),
        ("itinerary", "Itinerary"),
        ("tip", "Tip"),
        ("inspiration", "Inspiration"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="community_posts")
    title = models.CharField(max_length=180)
    body = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="question", db_index=True)
    city = models.ForeignKey(
        "destinations.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="community_posts",
    )
    is_published = models.BooleanField(default=True, db_index=True)
    comments_enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["category", "-created_at"]),
            models.Index(fields=["is_published", "-created_at"]),
        ]

    def __str__(self):
        return self.title


class CommunityReply(AuditModel):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="community_replies")
    body = models.TextField(max_length=3000)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    is_published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Reply by {self.author} on {self.post}"


class CommunityLike(AuditModel):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="community_likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique_community_post_like"),
        ]


class CommunitySave(AuditModel):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name="saves")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="community_saves")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique_community_post_save"),
        ]


class CommunityReport(AuditModel):
    REASON_CHOICES = [
        ("spam", "Spam"),
        ("abuse", "Harassment or abuse"),
        ("misleading", "Misleading information"),
        ("other", "Other"),
    ]

    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name="reports")
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="community_reports")
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    note = models.TextField(blank=True, max_length=1000)
    status = models.CharField(max_length=20, default="open", db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "reporter"], name="unique_community_post_report"),
        ]


class CommunityReplyLike(AuditModel):
    reply = models.ForeignKey(CommunityReply, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="community_reply_likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["reply", "user"], name="unique_community_reply_like"),
        ]


class CommunityNotification(AuditModel):
    TYPE_CHOICES = [
        ("post_reply", "Reply to your post"),
        ("reply_reply", "Reply to your comment"),
        ("post_like", "Like on your post"),
        ("reply_like", "Like on your comment"),
        ("mention", "Mention"),
        ("trip_created", "Trip created"),
        ("trip_updated", "Trip updated"),
        ("trip_shared", "Trip shared"),
        ("budget_alert", "Budget alert"),
        ("system", "Workspace update"),
    ]

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="community_notifications"
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="community_notification_actions",
    )
    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )
    reply = models.ForeignKey(
        CommunityReply,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
    )
    kind = models.CharField(max_length=20, choices=TYPE_CHOICES, db_index=True)
    message = models.CharField(max_length=240)
    url = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read", "-created_at"]),
            models.Index(fields=["recipient", "-created_at"]),
        ]


class CommunityShare(AuditModel):
    CHANNEL_CHOICES = [
        ("copy", "Copy link"),
        ("native", "Device share"),
        ("whatsapp", "WhatsApp"),
        ("email", "Email"),
    ]

    post = models.ForeignKey(
        CommunityPost, on_delete=models.CASCADE, related_name="shares"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="community_shares"
    )
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
