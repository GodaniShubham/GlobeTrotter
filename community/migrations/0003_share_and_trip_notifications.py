from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("community", "0002_social_realtime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="communitynotification",
            name="kind",
            field=models.CharField(
                max_length=20,
                db_index=True,
                choices=[
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
                ],
            ),
        ),
        migrations.CreateModel(
            name="CommunityShare",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_ip", models.GenericIPAddressField(blank=True, help_text="IP address of the creator", null=True)),
                ("created_location", models.CharField(blank=True, help_text="Approximate location of the creator", max_length=255, null=True)),
                ("channel", models.CharField(choices=[("copy", "Copy link"), ("native", "Device share"), ("whatsapp", "WhatsApp"), ("email", "Email")], max_length=20)),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="shares", to="community.communitypost")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="community_shares", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
