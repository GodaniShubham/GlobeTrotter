from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("community", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CommunityNotification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_ip", models.GenericIPAddressField(blank=True, help_text="IP address of the creator", null=True)),
                ("created_location", models.CharField(blank=True, help_text="Approximate location of the creator", max_length=255, null=True)),
                ("kind", models.CharField(
                    choices=[
                        ("post_reply", "Reply to your post"),
                        ("reply_reply", "Reply to your comment"),
                        ("post_like", "Like on your post"),
                        ("reply_like", "Like on your comment"),
                        ("mention", "Mention"),
                    ],
                    db_index=True,
                    max_length=20,
                )),
                ("message", models.CharField(max_length=240)),
                ("url", models.CharField(max_length=500)),
                ("is_read", models.BooleanField(db_index=True, default=False)),
                ("actor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="community_notification_actions", to=settings.AUTH_USER_MODEL)),
                ("post", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to="community.communitypost")),
                ("recipient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="community_notifications", to=settings.AUTH_USER_MODEL)),
                ("reply", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="notifications", to="community.communityreply")),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["recipient", "is_read", "-created_at"], name="community_c_recipient_56a6cb_idx"),
                    models.Index(fields=["recipient", "-created_at"], name="community_c_recipient_4be6e4_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="CommunityReplyLike",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_ip", models.GenericIPAddressField(blank=True, help_text="IP address of the creator", null=True)),
                ("created_location", models.CharField(blank=True, help_text="Approximate location of the creator", max_length=255, null=True)),
                ("reply", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="community.communityreply")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="community_reply_likes", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(fields=("reply", "user"), name="unique_community_reply_like")
                ]
            },
        ),
    ]
