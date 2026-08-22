from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import (
    CommunityLike,
    CommunityNotification,
    CommunityPost,
    CommunityReply,
    CommunityReplyLike,
    CommunitySave,
)


class CommunityProductionFlowTests(TestCase):
    def setUp(self):
        self.alex = User.objects.create_user(
            username="alex",
            first_name="Alex",
            last_name="Kapoor",
            email="alex@example.com",
            password="StrongPass123!",
        )
        self.maya = User.objects.create_user(
            username="maya",
            first_name="Maya",
            last_name="Joseph",
            email="maya@example.com",
            password="StrongPass123!",
        )
        self.post = CommunityPost.objects.create(
            author=self.maya,
            title="Best areas to stay in Kyoto?",
            body="Looking for a walkable neighbourhood with good food and easy morning access to temples.",
            category="question",
        )

    def test_feed_sort_and_search(self):
        self.client.force_login(self.alex)
        response = self.client.get(reverse("community"), {"q": "Kyoto", "sort": "new"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_create_post_persists_and_supports_mentions(self):
        self.client.force_login(self.alex)
        response = self.client.post(reverse("community_new"), {
            "title": "A useful Kyoto morning idea",
            "category": "tip",
            "city": "",
            "body": "@maya Try an early Fushimi Inari visit before breakfast.",
        })
        self.assertEqual(response.status_code, 302)
        created = CommunityPost.objects.get(author=self.alex, title__startswith="A useful Kyoto")
        self.assertTrue(
            CommunityNotification.objects.filter(
                recipient=self.maya, actor=self.alex, kind="mention", post=created
            ).exists()
        )

    def test_reply_creates_notification_and_supports_nested_reply(self):
        self.client.force_login(self.alex)
        response = self.client.post(
            reverse("community_reply", args=[self.post.pk]),
            {"body": "I would stay around Gion for walkability."},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        parent = CommunityReply.objects.get(post=self.post, author=self.alex)
        self.assertTrue(
            CommunityNotification.objects.filter(
                recipient=self.maya, kind="post_reply", reply=parent
            ).exists()
        )

        response = self.client.post(
            reverse("community_reply", args=[self.post.pk]),
            {"body": "Agreed — especially for early mornings.", "parent_id": parent.pk},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        child = CommunityReply.objects.get(parent=parent)
        self.assertTrue(child.parent_id == parent.pk)

    def test_post_like_notifies_author(self):
        self.client.force_login(self.alex)
        response = self.client.post(reverse("community_like", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CommunityLike.objects.filter(post=self.post, user=self.alex).exists())
        self.assertTrue(
            CommunityNotification.objects.filter(
                recipient=self.maya, actor=self.alex, kind="post_like", post=self.post
            ).exists()
        )

    def test_reply_like_notifies_author(self):
        reply = CommunityReply.objects.create(
            post=self.post, author=self.maya,
            body="Try Gion or Higashiyama for a first visit."
        )
        self.client.force_login(self.alex)
        response = self.client.post(reverse("community_reply_like", args=[reply.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CommunityReplyLike.objects.filter(reply=reply, user=self.alex).exists())
        self.assertTrue(
            CommunityNotification.objects.filter(
                recipient=self.maya, actor=self.alex, kind="reply_like", reply=reply
            ).exists()
        )

    def test_notification_feed_and_mark_read(self):
        CommunityNotification.objects.create(
            recipient=self.alex,
            actor=self.maya,
            post=self.post,
            kind="post_reply",
            message="Maya replied to your post.",
            url=reverse("community_post", args=[self.post.pk]),
        )
        self.client.force_login(self.alex)
        response = self.client.get(reverse("community_notifications"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["unread"], 1)

        response = self.client.post(reverse("community_notifications_read"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            CommunityNotification.objects.filter(recipient=self.alex, is_read=False).count(),
            0,
        )

    def test_post_updates_returns_nested_replies(self):
        parent = CommunityReply.objects.create(
            post=self.post, author=self.alex, body="A useful reply."
        )
        CommunityReply.objects.create(
            post=self.post, author=self.maya, parent=parent, body="A useful follow-up."
        )
        self.client.force_login(self.alex)
        response = self.client.get(reverse("community_updates", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["reply_count"], 2)
        self.assertEqual(response.json()["replies"][1]["parent_id"], parent.pk)


class ShareNotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="share_user", password="StrongPass123!")
        self.post = CommunityPost.objects.create(
            author=self.user,
            title="Shareable Kyoto thread",
            body="A useful community post for testing sharing.",
            category="question",
        )
        self.client.force_login(self.user)

    def test_record_share(self):
        response = self.client.post(
            reverse("community_share", args=[self.post.pk]),
            {"channel": "copy"},
        )
        self.assertEqual(response.status_code, 200)
        from .models import CommunityShare
        self.assertTrue(CommunityShare.objects.filter(post=self.post, user=self.user, channel="copy").exists())
