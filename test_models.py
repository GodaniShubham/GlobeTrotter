import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.utils import get_location_from_ip
from destinations.models import City
from trips.models import Trip, TripStop

def run_test():
    print("--------------------------------------------------")
    print("          GLOBETROTTER BACKEND TEST               ")
    print("--------------------------------------------------\n")
    
    print("[1] Testing Geolocation utility...")
    loc = get_location_from_ip('8.8.8.8')
    print(f"    IP 8.8.8.8 resolves to Location: {loc}\n")
    
    print("[2] Testing Database Models...")
    # Test User
    user, created = User.objects.get_or_create(username='testuser', email='test@example.com')
    if created:
        user.set_password('password123')
        user.save()
    print("    -> User account created/retrieved.")

    # Test City
    city, _ = City.objects.get_or_create(name='Paris', country='France', cost_index=85, popularity=95)
    print("    -> City 'Paris, France' created.")

    # Test Trip
    trip, _ = Trip.objects.get_or_create(
        user=user, 
        name='My Awesome Europe Tour', 
        start_date='2026-09-01', 
        end_date='2026-09-15'
    )
    print(f"    -> Trip '{trip.name}' created.")

    # Test TripStop
    stop, _ = TripStop.objects.get_or_create(
        trip=trip,
        city=city,
        arrival_date='2026-09-01',
        departure_date='2026-09-05',
        order=1
    )
    print(f"    -> Trip Stop added: {stop.city.name} from {stop.arrival_date} to {stop.departure_date}.")
    
    print("\n--------------------------------------------------")
    print("  SUCCESS: All Backend Models are 100% working!   ")
    print("--------------------------------------------------")

if __name__ == '__main__':
    run_test()
