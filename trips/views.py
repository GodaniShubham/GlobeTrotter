from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Trip, TripStop
from django.contrib import messages
from django.utils import timezone

@login_required
def dashboard_view(request):
    trips = Trip.objects.filter(user=request.user).order_by('start_date')
    upcoming_trips = [t for t in trips if t.start_date and t.start_date >= timezone.now().date()]
    past_trips = [t for t in trips if t.start_date and t.start_date < timezone.now().date()]
    
    # Calculate some basic stats
    countries_visited = 0 # Can be calculated based on cities
    cities_explored = 0
    
    context = {
        'page_title': 'Dashboard — GlobeTrotter',
        'active': 'dashboard',
        'upcoming_trips': upcoming_trips,
        'past_trips': past_trips,
        'total_trips': len(trips),
        'countries_visited': countries_visited,
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
        name = request.POST.get('name')
        start_date = request.POST.get('start_date') or None
        end_date = request.POST.get('end_date') or None
        
        if name:
            trip = Trip.objects.create(
                user=request.user,
                name=name,
                start_date=start_date,
                end_date=end_date,
            )
            messages.success(request, f'Trip "{trip.name}" created! Start adding destinations.')
            # After creating, redirect to the builder (we will need to pass the trip ID later)
            return redirect('builder')
        else:
            messages.error(request, 'Trip name is required.')
            
    context = {
        'page_title': 'Create trip — GlobeTrotter',
        'active': 'create'
    }
    return render(request, "pages/create_trip.html", context)

@login_required
def builder_view(request):
    # For now, just render the builder UI
    # In Phase 3, we will pass a specific trip ID
    context = {
        'page_title': 'Itinerary builder — GlobeTrotter',
        'active': 'builder'
    }
    return render(request, "pages/builder.html", context)

@login_required
def itinerary_view(request):
    context = {
        'page_title': 'Itinerary view — GlobeTrotter',
        'active': 'itinerary'
    }
    return render(request, "pages/itinerary.html", context)
