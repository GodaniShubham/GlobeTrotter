import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from destinations.models import City
from activities.models import Activity
from django.contrib.auth.models import User
from trips.models import Trip, TripStop, ItineraryActivity

def run():
    print("Seeding Indian Cities...")
    indian_cities = [
        ("Mumbai", "Maharashtra", 8, 98, "The city of dreams"),
        ("Delhi", "Delhi", 7, 97, "The heart of India"),
        ("Bangalore", "Karnataka", 7, 95, "Silicon Valley of India"),
        ("Hyderabad", "Telangana", 6, 92, "City of Pearls"),
        ("Ahmedabad", "Gujarat", 6, 88, "Manchester of India"),
        ("Chennai", "Tamil Nadu", 7, 90, "Gateway to South India"),
        ("Kolkata", "West Bengal", 6, 89, "City of Joy"),
        ("Surat", "Gujarat", 5, 80, "Diamond City of India"),
        ("Pune", "Maharashtra", 6, 85, "Oxford of the East"),
        ("Jaipur", "Rajasthan", 6, 94, "The Pink City"),
        ("Lucknow", "Uttar Pradesh", 5, 78, "City of Nawabs"),
        ("Kanpur", "Uttar Pradesh", 5, 75, "Leather City of the World"),
        ("Nagpur", "Maharashtra", 5, 76, "Orange City"),
        ("Indore", "Madhya Pradesh", 5, 82, "Cleanest City of India"),
        ("Thane", "Maharashtra", 6, 70, "City of Lakes"),
        ("Bhopal", "Madhya Pradesh", 5, 79, "City of Lakes"),
        ("Visakhapatnam", "Andhra Pradesh", 5, 81, "City of Destiny"),
        ("Pimpri-Chinchwad", "Maharashtra", 5, 68, "Industrial City"),
        ("Patna", "Bihar", 4, 72, "Ancient city of Pataliputra"),
        ("Vadodara", "Gujarat", 5, 77, "Cultural Capital of Gujarat"),
        ("Ghaziabad", "Uttar Pradesh", 5, 65, "Gateway of UP"),
        ("Ludhiana", "Punjab", 5, 74, "Manchester of India"),
        ("Agra", "Uttar Pradesh", 5, 96, "Home to the Taj Mahal"),
        ("Nashik", "Maharashtra", 5, 83, "Wine Capital of India"),
        ("Faridabad", "Haryana", 5, 66, "Industrial Hub"),
        ("Meerut", "Uttar Pradesh", 4, 69, "Sports City of India"),
        ("Rajkot", "Gujarat", 5, 73, "Colourful City"),
        ("Kalyan-Dombivli", "Maharashtra", 5, 60, "Twin Cities"),
        ("Vasai-Virar", "Maharashtra", 5, 62, "Historical Suburb"),
        ("Varanasi", "Uttar Pradesh", 5, 95, "Spiritual Capital of India")
    ]

    cities = []
    for idx, (name, state, cost, pop, desc) in enumerate(indian_cities):
        city, _ = City.objects.get_or_create(
            name=name,
            country="India",
            defaults={"cost_index": cost, "popularity": pop, "description": desc}
        )
        cities.append(city)

    print("Seeding Activities...")
    activity_types = ["Sightseeing", "Adventure", "Relaxation", "Food Tours", "Experience"]
    for city in cities:
        for i in range(1, 4):
            Activity.objects.get_or_create(
                city=city,
                name=f"{city.name} {random.choice(activity_types)} Tour",
                activity_type=random.choice(activity_types),
                estimated_cost=random.randint(500, 5000),
                duration=random.randint(2, 8)
            )
            
    print("Seeding Users for Growth Chart...")
    now = timezone.now()
    for i in range(1, 20):
        weeks_ago = random.randint(0, 7) # Stagger over last 8 weeks
        email = f"user_{i}@example.com"
        user, created = User.objects.get_or_create(username=f"user_{i}", email=email)
        if created:
            user.set_password("pass123")
            # Override date_joined (save skips auto_now_add if we force update)
            user.date_joined = now - timedelta(weeks=weeks_ago, days=random.randint(0, 6))
            user.save(update_fields=['date_joined'])
            
    print("Seeding Default Itinerary (Golden Triangle)...")
    admin_user = User.objects.filter(email='admin@globetrotter.com').first() or user
    
    trip, _ = Trip.objects.get_or_create(
        user=admin_user,
        name="Golden Triangle Explorer",
        defaults={
            "description": "A classic tour of Delhi, Agra, and Jaipur.",
            "start_date": (now + timedelta(days=10)).date(),
            "end_date": (now + timedelta(days=17)).date(),
            "is_public": True
        }
    )
    
    # Get specific cities
    delhi = City.objects.filter(name="Delhi").first()
    agra = City.objects.filter(name="Agra").first()
    jaipur = City.objects.filter(name="Jaipur").first()
    
    if delhi and agra and jaipur:
        TripStop.objects.get_or_create(trip=trip, city=delhi, arrival_date=trip.start_date, departure_date=trip.start_date + timedelta(days=2), order=1)
        TripStop.objects.get_or_create(trip=trip, city=agra, arrival_date=trip.start_date + timedelta(days=2), departure_date=trip.start_date + timedelta(days=4), order=2)
        TripStop.objects.get_or_create(trip=trip, city=jaipur, arrival_date=trip.start_date + timedelta(days=4), departure_date=trip.end_date, order=3)
    
        # Seed itinerary activities for Delhi Stop
        delhi_stop = trip.stops.first()
        delhi_act = delhi.activities.first()
        if delhi_stop and delhi_act:
            ItineraryActivity.objects.get_or_create(
                trip_stop=delhi_stop,
                activity=delhi_act,
                date=trip.start_date,
                order=1
            )
            
    print("Done!")

if __name__ == '__main__':
    run()
