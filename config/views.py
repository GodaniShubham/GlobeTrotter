from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


def page(template, title="GlobeTrotter", **context):
    context.setdefault("page_title", title)
    return render(None, template, context)


def _render(request, template, title, **context):
    context.setdefault("page_title", title)
    return render(request, template, context)

def forgot_password(request):
    return render(request, "pages/forgot_password.html")
def community(request):
    return render(request, "pages/community.html")
def landing(request):
    from trips.models import Trip
    public_trip = Trip.objects.filter(is_public=True).first()
    if not public_trip:
        public_trip = Trip.objects.first() # fallback to any trip for the demo
        
    context = {
        'public_trip': public_trip
    }
    return render(request, "pages/landing.html", context)


def login_view(request):
    return _render(request, "pages/auth.html", "Sign in — GlobeTrotter", auth_mode="login")


def signup_view(request):
    return _render(request, "pages/auth.html", "Create account — GlobeTrotter", auth_mode="signup")


def dashboard(request):
    return _render(request, "pages/dashboard.html", "Dashboard — GlobeTrotter", active="dashboard")


def create_trip(request):
    return _render(request, "pages/create_trip.html", "Create trip — GlobeTrotter", active="create")


def trips(request):
    return _render(request, "pages/trips.html", "My trips — GlobeTrotter", active="trips")


def builder(request):
    return _render(request, "pages/builder.html", "Itinerary builder — GlobeTrotter", active="builder")


def itinerary(request):
    return _render(request, "pages/itinerary.html", "Itinerary view — GlobeTrotter", active="itinerary")


def city_search(request):
    return _render(request, "pages/city_search.html", "Discover cities — GlobeTrotter", active="cities")


def activity_search(request):
    return _render(request, "pages/activity_search.html", "Discover activities — GlobeTrotter", active="activities")


@login_required
def budget(request, trip_id):
    from trips.models import Trip
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    stops = trip.stops.prefetch_related('itinerary_activities').all()
    
    total_cost = 0
    cat_totals = {'Activities': 0, 'Transport': 0, 'Accommodation': 0, 'Meals': 0, 'Other': 0}
    
    for stop in stops:
        for it_act in stop.itinerary_activities.all():
            cost = float(it_act.custom_cost or it_act.activity.estimated_cost or 0)
            total_cost += cost
            cat = it_act.activity.activity_type
            if cat in cat_totals:
                cat_totals[cat] += cost
            else:
                cat_totals['Other'] += cost
                
    context = {
        'page_title': f'{trip.name} Budget — GlobeTrotter',
        'active': 'budget',
        'trip': trip,
        'total_cost': total_cost,
        'cat_totals': cat_totals
    }
    return render(request, "pages/budget.html", context)


@login_required
def calendar_view(request, trip_id):
    from trips.models import Trip
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    context = {
        'page_title': f'{trip.name} Calendar — GlobeTrotter',
        'active': 'calendar',
        'trip': trip
    }
    return render(request, "pages/calendar.html", context)


def public_itinerary(request, trip_id):
    from trips.models import Trip
    trip = get_object_or_404(Trip, id=trip_id, is_public=True)
    stops = trip.stops.prefetch_related('itinerary_activities__activity').all()
    context = {
        'page_title': f'{trip.name} — GlobeTrotter',
        'trip': trip,
        'stops': stops
    }
    return render(request, "pages/public_itinerary.html", context)


def profile(request):
    return _render(request, "pages/profile.html", "Profile & settings — GlobeTrotter", active="profile")


def admin_dashboard(request):
    return _render(request, "pages/admin_dashboard.html", "Analytics — GlobeTrotter", active="admin")
