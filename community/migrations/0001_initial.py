# Generated manually for GlobeTrotter Community.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0002_alter_userprofile_id"),
        ("destinations", "0003_alter_city_id_alter_saveddestination_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommunityPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_ip", models.GenericIPAddressField(blank=True, help_text="IP address of the creator", null=True)),
                ("created_location", models.CharField(blank=True, help_text="Approximate location of the creator", max_length=255, null=True)),
                ("title", models.CharField(max_length=180)),
                ("body", models.TextField()),
                ("category", models.CharField(choices=[("question", "Question"), ("destination", "Destination"), ("itinerary", "Itinerary"), ("tip", "Tip"), ("inspiration", "Inspiration")], db_index=True, default="question", max_length=20)),
                ("is_published", models.BooleanField(db_index=True, default=True)),
                ("comments_enabled", models.BooleanField(default=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="community_posts", to=settings.AUTH_USER_MODEL)),
                ("city", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="community_posts", to="destinations.city")),
            ],
            options={"ordering": ["-created_at"], "indexes": [models.Index(fields=["category", "-created_at"], name="community_c_category_7ae2f6_idx"), models.Index(fields=["is_published", "-created_at"], name="community_c_is_published_8e41e8_idx")]},
        ),
        migrations.CreateModel(
            name="CommunityReply",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_ip", models.GenericIPAddressField(blank=True, help_text="IP address of the creator", null=True)),
                ("created_location", models.CharField(blank=True, help_text="Approximate location of the creator", max_length=255, null=True)),
                ("body", models.TextField(max_length=3000)),
                ("is_published", models.BooleanField(db_index=True, default=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="community_replies", to=settings.AUTH_USER_MODEL)),
                ("parent", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="children", to="community.communityreply")),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="replies", to="community.communitypost")),
            ],
            options={"ordering": ["created_at"]},
        ),
        migrations.CreateModel(
            name="CommunityLike",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_ip", models.GenericIPAddressField(blank=True, help_text="IP address of the creator", null=True)),
                ("created_location", models.CharField(blank=True, help_text="Approximate location of the creator", max_length=255, null=True)),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="community.communitypost")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="community_likes", to=settings.AUTH_USER_MODEL)),
            ],
            options={"constraints": [models.UniqueConstraint(fields=("post", "user"), name="unique_community_post_like")]},
        ),
        migrations.CreateModel(
            name="CommunitySave",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_ip", models.GenericIPAddressField(blank=True, help_text="IP address of the creator", null=True)),
                ("created_location", models.CharField(blank=True, help_text="Approximate location of the creator", max_length=255, null=True)),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="saves", to="community.communitypost")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="community_saves", to=settings.AUTH_USER_MODEL)),
            ],
            options={"constraints": [models.UniqueConstraint(fields=("post", "user"), name="unique_community_post_save")]},
        ),
        migrations.CreateModel(
            name="CommunityReport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_ip", models.GenericIPAddressField(blank=True, help_text="IP address of the creator", null=True)),
                ("created_location", models.CharField(blank=True, help_text="Approximate location of the creator", max_length=255, null=True)),
                ("reason", models.CharField(choices=[("spam", "Spam"), ("abuse", "Harassment or abuse"), ("misleading", "Misleading information"), ("other", "Other")], max_length=20)),
                ("note", models.TextField(blank=True, max_length=1000)),
                ("status", models.CharField(db_index=True, default="open", max_length=20)),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reports", to="community.communitypost")),
                ("reporter", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="community_reports", to=settings.AUTH_USER_MODEL)),
            ],
            options={"constraints": [models.UniqueConstraint(fields=("post", "reporter"), name="unique_community_post_report")]},
        ),
    ]
