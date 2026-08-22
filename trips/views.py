from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trip, TripStop, ItineraryActivity
from destinations.models import City
from activities.models import Activity
from django.contrib import messages
from django.utils import timezone
from core.ai_generator import generate_itinerary
import datetime

@login_required
def dashboard_view(request):
    trips = Trip.objects.filter(user=request.user).order_by('start_date')
    upcoming_trips = [t for t in trips if t.start_date and t.start_date >= timezone.now().date()]
    past_trips = [t for t in trips if t.start_date and t.start_date < timezone.now().date()]
    
    cities_explored = TripStop.objects.filter(trip__user=request.user).values('city').distinct().count()
    
    context = {
        'page_title': 'Dashboard — GlobeTrotter',
        'active': 'dashboard',
        'upcoming_trips': upcoming_trips,
        'past_trips': past_trips,
        'total_trips': len(trips),
        'cities_explored': cities_explored
    }
    return render(request, "pages/dashboard.html", context)

@login_required
def trips_view(request):
    trips = Trip.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'page_title': 'My trips — GlobeTrotter',
        'active': 'trips',
        'trips': trips
    }
    return render(request, "pages/trips.html", context)

@login_required
def create_trip_view(request):
    if request.method == 'POST':
        destination = request.POST.get('destination')
        days = request.POST.get('days')
        pace = request.POST.get('pace')
        interests = request.POST.get('interests')
        start_date_str = request.POST.get('start_date')
        
        if not destination or not days or not start_date_str:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('create_trip')
            
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = start_date + datetime.timedelta(days=int(days))
            
            # Generate via Groq
            ai_data = generate_itinerary(destination, days, pace, interests)
            
            # Create the Trip
            trip = Trip.objects.create(
                user=request.user,
                name=ai_data.get('trip_name', f'Trip to {destination}'),
                description=ai_data.get('description', ''),
                start_date=start_date,
                end_date=end_date,
            )
            
            # Create Stops and Activities
            current_date = start_date
            order = 1
            for city_data in ai_data.get('cities', []):
                city_name = city_data.get('name', 'Unknown City')
                city_days = int(city_data.get('days', 1))
                
                # Get or create City
                city_obj, _ = City.objects.get_or_create(name=city_name, defaults={'country': destination})
                
                # Create TripStop
                stop_end_date = current_date + datetime.timedelta(days=city_days)
                trip_stop = TripStop.objects.create(
                    trip=trip,
                    city=city_obj,
                    arrival_date=current_date,
                    departure_date=stop_end_date,
                    order=order
                )
                
                # Create Activities
                act_order = 1
                for act_data in city_data.get('activities', []):
                    act_name = act_data.get('name', 'Activity')
                    act_desc = act_data.get('description', '')
                    act_cost = float(act_data.get('cost_estimate_usd', 0.0))
                    act_cat = act_data.get('category', 'Activities')
                    
                    # Get or create Activity
                    activity_obj, _ = Activity.objects.get_or_create(
                        name=act_name, city=city_obj, 
                        defaults={'description': act_desc, 'estimated_cost': act_cost, 'activity_type': 'Sightseeing'}
                    )
                    
                    # Add to itinerary
                    ItineraryActivity.objects.create(
                        trip_stop=trip_stop,
                        activity=activity_obj,
                        date=current_date, # Put them on the first day of the stop for simplicity initially
                        custom_cost=act_cost,
                        order=act_order
                    )
                    act_order += 1
                
                current_date = stop_end_date
                order += 1
                
            messages.success(request, f'AI generated your "{trip.name}" trip successfully!')
            return redirect('builder')
            
        except Exception as e:
            messages.error(request, f"AI Generation Failed: {str(e)}")
            return redirect('create_trip')
            
    context = {
        'page_title': 'Create trip — GlobeTrotter',
        'active': 'create'
    }
    return render(request, "pages/create_trip.html", context)

@login_required
def builder_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    context = {
        'page_title': f'{trip.name} Builder — GlobeTrotter',
        'active': 'builder',
        'trip': trip
    }
    return render(request, "pages/builder.html", context)

@login_required
def itinerary_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    stops = trip.stops.prefetch_related('itinerary_activities__activity').all()
    
    context = {
        'page_title': f'{trip.name} Itinerary — GlobeTrotter',
        'active': 'itinerary',
        'trip': trip,
        'stops': stops
    }
    return render(request, "pages/itinerary.html", context)
