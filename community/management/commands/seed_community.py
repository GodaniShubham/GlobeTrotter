from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from community.models import CommunityPost

class Command(BaseCommand):
    help = "Create a small idempotent set of community demo posts for local/staging testing."

    def add_arguments(self, parser):
        parser.add_argument("--username", help="Existing Django username to own the demo posts.")
        parser.add_argument("--clear-demo", action="store_true", help="Remove only demo posts created by this command before reseeding.")

    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get("username")
        user = User.objects.filter(username=username).first() if username else User.objects.order_by("pk").first()

        if user is None:
            raise CommandError("No user exists. Create/login a user first, then run this command again.")

        titles = [
            ("Is 7 days enough for Tokyo, Kyoto and Osaka?", "question", "I’m planning a first Japan trip and want two slower mornings without missing the classics. How would you divide the days?"),
            ("Best scenic rail segments between Zurich and Interlaken?", "destination", "Looking for the most beautiful route rather than the fastest one, with easy stopovers."),
            ("One neighbourhood in Lisbon you would never skip?", "tip", "I want one local, walkable area for a short city break without rushing."),
            ("How much empty time do you leave in a day?", "inspiration", "I’m experimenting with one open block each day so the itinerary feels less like a checklist."),
        ]

        if options["clear_demo"]:
            CommunityPost.objects.filter(
                author=user,
                title__in=[t[0] for t in titles],
            ).delete()

        created = 0
        for title, category, body in titles:
            post, was_created = CommunityPost.objects.get_or_create(
                author=user,
                title=title,
                defaults={
                    "category": category,
                    "body": body,
                    "is_published": True,
                    "comments_enabled": True,
                },
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f"Community demo data ready for user '{user.username}'. Created {created} new posts."
        ))
