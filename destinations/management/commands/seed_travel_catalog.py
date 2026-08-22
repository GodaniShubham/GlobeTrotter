
from django.core.management.base import BaseCommand
from django.db import transaction

from destinations.models import City
from activities.models import Activity


CITY_IMAGES = {'Tokyo': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=1200&q=85', 'Kyoto': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=85', 'Osaka': 'https://images.unsplash.com/photo-1590559899731-a382839e5549?auto=format&fit=crop&w=1200&q=85', 'Paris': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1200&q=85', 'Rome': 'https://images.unsplash.com/photo-1529260830199-42c24126f198?auto=format&fit=crop&w=1200&q=85', 'Barcelona': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?auto=format&fit=crop&w=1200&q=85', 'Lisbon': 'https://images.unsplash.com/photo-1555881400-74d7acaacd8b?auto=format&fit=crop&w=1200&q=85', 'Dubai': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=85', 'Bali': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=85', 'Singapore': 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1200&q=85', 'New York': 'https://images.unsplash.com/photo-1496588152823-86ff7695e68f?auto=format&fit=crop&w=1200&q=85', 'Cape Town': 'https://images.unsplash.com/photo-1580060839134-75a5edca2e99?auto=format&fit=crop&w=1200&q=85', 'Sydney': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d4?auto=format&fit=crop&w=1200&q=85', 'Istanbul': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1200&q=85', 'Bangkok': 'https://images.unsplash.com/photo-1508009603885-50cf7c579365?auto=format&fit=crop&w=1200&q=85', 'Zurich': 'https://images.unsplash.com/photo-1515488764276-beab7607c1e6?auto=format&fit=crop&w=1200&q=85', 'Reykjavik': 'https://images.unsplash.com/photo-1530789253388-582c481c54b0?auto=format&fit=crop&w=1200&q=85', 'Vancouver': 'https://images.unsplash.com/photo-1559511260-66a654ae982a?auto=format&fit=crop&w=1200&q=85'}

ACTIVITY_IMAGES = {'Sightseeing': 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1200&q=85', 'Food': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=85', 'Museum': 'https://images.unsplash.com/photo-1561214115-f2f134cc4912?auto=format&fit=crop&w=1200&q=85', 'Adventure': 'https://images.unsplash.com/photo-1501554728187-4e197c1b7f3e?auto=format&fit=crop&w=1200&q=85', 'Shopping': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1200&q=85', 'Nature': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=85', 'Entertainment': 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=85', 'Nightlife': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=1200&q=85', 'Other': 'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=85'}

CITIES = [('Tokyo', 'Japan', 'Asia', 'Neon districts, historic neighbourhoods, exceptional food and a huge variety of day-trip options.', 85, 100), ('Kyoto', 'Japan', 'Asia', 'Temples, traditional streets, gardens, tea culture and slower mornings.', 80, 96), ('Osaka', 'Japan', 'Asia', 'Food-first city breaks, lively neighbourhoods, markets and nightlife.', 72, 92), ('Paris', 'France', 'Europe', 'Museums, architecture, neighbourhood walks, cafés and iconic landmarks.', 88, 100), ('Rome', 'Italy', 'Europe', 'Ancient history, piazzas, museums, food and walkable central districts.', 82, 99), ('Barcelona', 'Spain', 'Europe', 'Gaudí architecture, Mediterranean food, beaches and lively neighbourhoods.', 76, 97), ('Lisbon', 'Portugal', 'Europe', 'Hillside viewpoints, trams, food markets and easy coastal escapes.', 68, 94), ('Dubai', 'United Arab Emirates', 'Middle East', 'Modern architecture, desert experiences, shopping and high-energy city days.', 92, 91), ('Bali', 'Indonesia', 'Asia', 'Beaches, temples, rice terraces, cafés, wellness and adventure.', 58, 95), ('Singapore', 'Singapore', 'Asia', 'Food, design, gardens, neighbourhood culture and efficient city exploration.', 78, 93), ('New York', 'United States', 'North America', 'Museums, neighbourhoods, food, skyline views and endless city activities.', 92, 98), ('Cape Town', 'South Africa', 'Africa', 'Coastal scenery, Table Mountain, food, wine and outdoor adventures.', 62, 90), ('Sydney', 'Australia', 'Oceania', 'Harbour views, beaches, coastal walks and urban culture.', 84, 89), ('Istanbul', 'Türkiye', 'Europe', 'Historic districts, bazaars, Bosphorus views and exceptional food culture.', 64, 95), ('Bangkok', 'Thailand', 'Asia', 'Street food, temples, markets, river life and energetic evenings.', 55, 97), ('Zurich', 'Switzerland', 'Europe', 'Lakefront walks, alpine access, design and polished city culture.', 94, 86), ('Reykjavik', 'Iceland', 'Europe', 'Compact city base for waterfalls, geothermal sites and northern landscapes.', 91, 84), ('Vancouver', 'Canada', 'North America', 'Mountains, sea, food culture and outdoor experiences close to the city.', 86, 88)]

ACTIVITY_BLUEPRINTS = [('Sightseeing', 'City highlights walking tour', 120, 1200), ('Food', 'Local market food crawl', 120, 900), ('Museum', 'Museum and gallery afternoon', 150, 1400), ('Nature', 'Scenic viewpoint and nature walk', 150, 700), ('Adventure', 'Guided outdoor adventure', 180, 2200), ('Shopping', 'Neighbourhood shopping walk', 120, 800), ('Entertainment', 'Evening cultural show', 150, 1800), ('Nightlife', 'Neighbourhood evening food & drinks', 150, 1600)]

SPECIALS = {'Tokyo': [('Food', 'Tsukiji Outer Market breakfast', 105, 1200), ('Sightseeing', 'Asakusa and Senso-ji walking route', 150, 600), ('Entertainment', 'Shibuya skyline sunset', 120, 1100), ('Shopping', 'Harajuku and Omotesando design walk', 150, 900)], 'Kyoto': [('Sightseeing', 'Fushimi Inari early morning walk', 150, 500), ('Sightseeing', 'Gion and Higashiyama temples', 180, 700), ('Food', 'Nishiki Market food tasting', 120, 1000), ('Nature', 'Arashiyama bamboo grove and river walk', 180, 600)], 'Osaka': [('Food', 'Kuromon Market food crawl', 120, 1200), ('Sightseeing', 'Osaka Castle and park', 150, 700), ('Entertainment', 'Dotonbori evening food route', 150, 1600), ('Shopping', 'Umeda neighbourhood shopping', 150, 1100)], 'Paris': [('Sightseeing', 'Louvre highlights', 180, 2200), ('Sightseeing', 'Montmartre and Sacré-Cœur walk', 150, 900), ('Food', 'Left Bank café and bakery crawl', 120, 1100), ('Museum', "Musée d'Orsay afternoon", 150, 1800)], 'Rome': [('Sightseeing', 'Colosseum and Roman Forum', 180, 2600), ('Food', 'Trastevere food walk', 150, 1400), ('Sightseeing', "Vatican Museums and St Peter's", 180, 3000), ('Nature', 'Villa Borghese park walk', 120, 500)], 'Barcelona': [('Sightseeing', 'Sagrada Família and Eixample', 180, 2200), ('Food', 'La Boqueria tasting route', 120, 1200), ('Nature', 'Barceloneta coastal walk', 120, 400), ('Sightseeing', 'Park Güell', 150, 1500)], 'Lisbon': [('Sightseeing', 'Alfama tram and viewpoint walk', 150, 700), ('Food', 'Pastéis and local food tasting', 120, 900), ('Sightseeing', 'Belém riverside landmarks', 150, 1100), ('Nature', 'Sintra day escape', 420, 3200)]}


class Command(BaseCommand):
    help = "Seed an idempotent GlobeTrotter city + activity catalog for local or MySQL development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete the seeded cities and their activities before recreating them.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            names = [row[0] for row in CITIES]
            Activity.objects.filter(city__name__in=names).delete()
            City.objects.filter(name__in=names).delete()

        created_cities = 0
        updated_cities = 0
        created_activities = 0
        updated_activities = 0

        for name, country, region, description, cost_index, popularity in CITIES:
            city, created = City.objects.get_or_create(
                name=name,
                country=country,
                defaults={
                    "region": region,
                    "description": description,
                    "cost_index": cost_index,
                    "popularity": popularity,
                },
            )

            changed = False
            updates = {
                "region": region,
                "description": description,
                "cost_index": cost_index,
                "popularity": popularity,
            }
            for field, value in updates.items():
                if getattr(city, field) != value:
                    setattr(city, field, value)
                    changed = True
            if changed:
                city.save(update_fields=list(updates.keys()) + ["updated_at"])

            if created:
                created_cities += 1
            elif changed:
                updated_cities += 1

            activity_rows = SPECIALS.get(name, []) + [
                (kind, f"{name} {label}", duration, cost)
                for kind, label, duration, cost in ACTIVITY_BLUEPRINTS
            ]

            for activity_type, activity_name, duration, cost in activity_rows:
                description_text = (
                    f"{activity_name} — a ready-to-plan experience in {name}. "
                    "Add it to a trip, assign a day and time, and adjust the cost if needed."
                )
                activity, a_created = Activity.objects.get_or_create(
                    city=city,
                    name=activity_name,
                    defaults={
                        "description": description_text,
                        "activity_type": activity_type,
                        "duration": duration,
                        "estimated_cost": cost,
                            "external_image_url": ACTIVITY_IMAGES.get(activity_type, ""),
                    },
                )
                a_changed = False
                a_updates = {
                    "description": description_text,
                    "activity_type": activity_type,
                    "duration": duration,
                    "estimated_cost": cost,
                }
                for field, value in a_updates.items():
                    if getattr(activity, field) != value:
                        setattr(activity, field, value)
                        a_changed = True
                if a_changed:
                    activity.save(update_fields=list(a_updates.keys()) + ["updated_at"])

                if a_created:
                    created_activities += 1
                elif a_changed:
                    updated_activities += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Catalog ready: "
                f"{created_cities} cities created, {updated_cities} cities updated; "
                f"{created_activities} activities created, {updated_activities} activities updated."
            )
        )
