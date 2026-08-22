from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Max, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from activities.models import Activity
from destinations.models import City
from .models import ItineraryActivity, Trip, TripStop


def _owned_trip(request, trip_id=None):
    qs = Trip.objects.filter(user=request.user)
    if trip_id:
        return get_object_or_404(qs, pk=trip_id)
    return qs.order_by("-created_at").first()


def _date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def _time(value):
    if not value:
        return None
    return datetime.strptime(value, "%H:%M").time()


def _trip_context(trip):
    stops = list(
        TripStop.objects.filter(trip=trip)
        .select_related("city")
        .prefetch_related(
            Prefetch(
                "itinerary_activities",
                queryset=ItineraryActivity.objects.select_related("activity", "activity__city")
                .order_by("date", "start_time", "order"),
            )
        )
        .order_by("order", "arrival_date")
    )
    activities = [item for stop in stops for item in stop.itinerary_activities.all()]
    unique_days = sorted({a.date for a in activities if a.date})
    total_cost = sum(
        float(a.custom_cost if a.custom_cost is not None else a.activity.estimated_cost or 0)
        for a in activities
    )
    return stops, activities, unique_days, total_cost


@login_required
def dashboard_view(request):
    trips = Trip.objects.filter(user=request.user).order_by("start_date")
    upcoming_trips = [t for t in trips if t.start_date and t.start_date >= timezone.now().date()]
    past_trips = [t for t in trips if t.start_date and t.start_date < timezone.now().date()]
    countries_visited = TripStop.objects.filter(
        trip__user=request.user
    ).values("city__country").distinct().count()
    cities_explored = TripStop.objects.filter(
        trip__user=request.user
    ).values("city_id").distinct().count()

    context = {
        "page_title": "Dashboard — GlobeTrotter",
        "active": "dashboard",
        "upcoming_trips": upcoming_trips,
        "past_trips": past_trips,
        "total_trips": len(trips),
        "countries_visited": countries_visited,
        "cities_explored": cities_explored,
    }
    return render(request, "pages/dashboard.html", context)


@login_required
def trips_view(request):
    trips = Trip.objects.filter(user=request.user).order_by("-created_at")
    return render(
        request,
        "pages/trips.html",
        {"page_title": "My trips — GlobeTrotter", "active": "trips", "trips": trips},
    )


@login_required
def create_trip_view(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        start_date = _date(request.POST.get("start_date"))
        end_date = _date(request.POST.get("end_date"))
        description = (request.POST.get("description") or "").strip()

        if not name or not start_date or not end_date:
            messages.error(request, "Trip name, start date and end date are required.")
        elif end_date < start_date:
            messages.error(request, "End date must be on or after the start date.")
        else:
            trip = Trip.objects.create(
                user=request.user,
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )
            messages.success(request, f'"{trip.name}" is ready. Start shaping the route.')
            return redirect(f"/trip/builder/?trip={trip.pk}")

    return render(
        request,
        "pages/create_trip.html",
        {"page_title": "Create trip — GlobeTrotter", "active": "create"},
    )


@login_required
def builder_view(request):
    trip = _owned_trip(request, request.GET.get("trip"))
    if not trip:
        messages.info(request, "Create a trip first, then start planning.")
        return redirect("create_trip")

    stops, activities, unique_days, total_cost = _trip_context(trip)
    cities = City.objects.order_by("name")
    return render(
        request,
        "pages/builder.html",
        {
            "page_title": f"{trip.name} — Itinerary builder",
            "active": "builder",
            "trip": trip,
            "stops": stops,
            "trip_activities": activities,
            "days_count": (trip.end_date - trip.start_date).days + 1,
            "unique_days": unique_days,
            "total_cost": total_cost,
            "cities": cities,
        },
    )


@login_required
def itinerary_view(request):
    trip = _owned_trip(request, request.GET.get("trip"))
    if not trip:
        messages.info(request, "Create a trip first.")
        return redirect("create_trip")

    stops, activities, unique_days, total_cost = _trip_context(trip)
    day_map = {}
    for activity in activities:
        if not activity.date:
            continue
        day_map.setdefault(activity.date, []).append(activity)

    itinerary_days = []
    current = trip.start_date
    while current <= trip.end_date:
        itinerary_days.append(
            {
                "date": current,
                "stop": next(
                    (
                        s
                        for s in stops
                        if s.arrival_date <= current <= s.departure_date
                    ),
                    None,
                ),
                "activities": day_map.get(current, []),
            }
        )
        current += timedelta(days=1)

    return render(
        request,
        "pages/itinerary.html",
        {
            "page_title": f"{trip.name} — Itinerary",
            "active": "itinerary",
            "trip": trip,
            "stops": stops,
            "itinerary_days": itinerary_days,
            "total_cost": total_cost,
            "days_count": (trip.end_date - trip.start_date).days + 1,
        },
    )


@login_required
@require_POST
def add_stop(request):
    trip = _owned_trip(request, request.POST.get("trip_id"))
    city = get_object_or_404(City, pk=request.POST.get("city_id"))

    if TripStop.objects.filter(trip=trip, city=city).exists():
        return JsonResponse({"ok": False, "message": f"{city.name} is already in this trip."}, status=400)

    last = TripStop.objects.filter(trip=trip).order_by("-order", "-departure_date").first()
    if last:
        arrival = last.departure_date
        departure = min(arrival + timedelta(days=2), trip.end_date)
        order = last.order + 1
    else:
        arrival = trip.start_date
        departure = min(trip.start_date + timedelta(days=2), trip.end_date)
        order = 1

    if departure < arrival:
        departure = arrival

    stop = TripStop.objects.create(
        trip=trip,
        city=city,
        arrival_date=arrival,
        departure_date=departure,
        order=order,
    )
    return JsonResponse(
        {
            "ok": True,
            "stop": {
                "id": stop.pk,
                "city": city.name,
                "country": city.country,
                "arrival": stop.arrival_date.isoformat(),
                "departure": stop.departure_date.isoformat(),
                "order": stop.order,
            },
        }
    )


@login_required
@require_POST
def update_stop(request, pk):
    stop = get_object_or_404(TripStop.objects.select_related("trip"), pk=pk, trip__user=request.user)
    arrival = _date(request.POST.get("arrival_date"))
    departure = _date(request.POST.get("departure_date"))
    if not arrival or not departure or departure < arrival:
        return JsonResponse({"ok": False, "message": "Choose valid arrival and departure dates."}, status=400)
    if arrival < stop.trip.start_date or departure > stop.trip.end_date:
        return JsonResponse({"ok": False, "message": "Stop dates must stay inside the trip dates."}, status=400)

    stop.arrival_date = arrival
    stop.departure_date = departure
    stop.save(update_fields=["arrival_date", "departure_date", "updated_at"])
    return JsonResponse({"ok": True})


@login_required
@require_POST
def reorder_stops(request):
    trip = _owned_trip(request, request.POST.get("trip_id"))
    raw_ids = [v for v in request.POST.getlist("stop_ids") if v.isdigit()]
    stops = list(TripStop.objects.filter(trip=trip, pk__in=raw_ids))
    if len(stops) != len(raw_ids):
        return JsonResponse({"ok": False, "message": "Invalid stop list."}, status=400)

    by_id = {str(s.pk): s for s in stops}
    with transaction.atomic():
        for index, stop_id in enumerate(raw_ids, start=1):
            stop = by_id[stop_id]
            stop.order = index
            stop.save(update_fields=["order", "updated_at"])
    return JsonResponse({"ok": True})


@login_required
@require_POST
def delete_stop(request, pk):
    stop = get_object_or_404(TripStop, pk=pk, trip__user=request.user)
    trip_id = stop.trip_id
    stop.delete()
    remaining = TripStop.objects.filter(trip_id=trip_id).order_by("order", "arrival_date")
    for index, item in enumerate(remaining, start=1):
        if item.order != index:
            item.order = index
            item.save(update_fields=["order", "updated_at"])
    return JsonResponse({"ok": True})


@login_required
@require_POST
def add_activity(request):
    stop = get_object_or_404(
        TripStop.objects.select_related("trip", "city"),
        pk=request.POST.get("trip_stop_id"),
        trip__user=request.user,
    )
    activity = get_object_or_404(Activity, pk=request.POST.get("activity_id"))

    if activity.city_id != stop.city_id:
        return JsonResponse(
            {
                "ok": False,
                "message": f"{activity.name} belongs to {activity.city.name}, not {stop.city.name}."
            },
            status=400,
        )

    date = _date(request.POST.get("date")) or stop.arrival_date
    start_time = _time(request.POST.get("start_time"))
    end_time = _time(request.POST.get("end_time"))
    if date < stop.arrival_date or date > stop.departure_date:
        return JsonResponse({"ok": False, "message": "Activity date must be inside the stop dates."}, status=400)
    if start_time and end_time and end_time <= start_time:
        return JsonResponse({"ok": False, "message": "End time must be after start time."}, status=400)

    next_order = (
        ItineraryActivity.objects.filter(trip_stop=stop, date=date)
        .aggregate(max_order=Max("order"))
        .get("max_order")
        or 0
    ) + 1

    row = ItineraryActivity.objects.create(
        trip_stop=stop,
        activity=activity,
        date=date,
        start_time=start_time,
        end_time=end_time,
        notes=(request.POST.get("notes") or "").strip(),
        custom_cost=request.POST.get("custom_cost") or None,
        order=next_order,
    )
    return JsonResponse(
        {
            "ok": True,
            "activity": {
                "id": row.pk,
                "name": activity.name,
                "city": activity.city.name,
                "date": date.isoformat(),
                "start_time": start_time.strftime("%H:%M") if start_time else "",
                "end_time": end_time.strftime("%H:%M") if end_time else "",
                "cost": float(row.custom_cost if row.custom_cost is not None else activity.estimated_cost),
            },
        }
    )


@login_required
@require_POST
def update_activity(request, pk):
    item = get_object_or_404(
        ItineraryActivity.objects.select_related("trip_stop", "trip_stop__trip"),
        pk=pk,
        trip_stop__trip__user=request.user,
    )
    date = _date(request.POST.get("date")) or item.date
    start_time = _time(request.POST.get("start_time"))
    end_time = _time(request.POST.get("end_time"))
    if date and not (item.trip_stop.arrival_date <= date <= item.trip_stop.departure_date):
        return JsonResponse({"ok": False, "message": "Activity date must stay inside the stop."}, status=400)
    if start_time and end_time and end_time <= start_time:
        return JsonResponse({"ok": False, "message": "End time must be after start time."}, status=400)

    item.date = date
    item.start_time = start_time
    item.end_time = end_time
    item.notes = (request.POST.get("notes") or item.notes).strip()
    if request.POST.get("custom_cost") not in (None, ""):
        item.custom_cost = request.POST.get("custom_cost")
    item.save(
        update_fields=[
            "date",
            "start_time",
            "end_time",
            "notes",
            "custom_cost",
            "updated_at",
        ]
    )
    return JsonResponse({"ok": True})


@login_required
@require_POST
def delete_activity(request, pk):
    item = get_object_or_404(
        ItineraryActivity,
        pk=pk,
        trip_stop__trip__user=request.user,
    )
    item.delete()
    return JsonResponse({"ok": True})


@login_required
def city_search_view(request):
    trip = _owned_trip(request, request.GET.get("trip"))
    q = (request.GET.get("q") or "").strip()
    region = (request.GET.get("region") or "").strip()

    from django.db.models import Count
    cities = City.objects.annotate(activity_count=Count("activities", distinct=True)).all()
    if q:
        cities = cities.filter(
            name__icontains=q
        ) | City.objects.filter(
            country__icontains=q
        )
    if region:
        cities = cities.filter(region__iexact=region)

    selected_city_ids = set(
        TripStop.objects.filter(trip=trip).values_list("city_id", flat=True)
    ) if trip else set()

    return render(
        request,
        "pages/city_search.html",
        {
            "page_title": "Discover cities — GlobeTrotter",
            "active": "cities",
            "cities": cities.distinct().order_by("-popularity", "name"),
            "trip": trip,
            "selected_city_ids": selected_city_ids,
            "regions": City.objects.exclude(region="").values_list("region", flat=True).distinct().order_by("region"),
        },
    )


@login_required
def activity_search_view(request):
    trip = _owned_trip(request, request.GET.get("trip"))
    selected_stop = None
    stop_id = request.GET.get("stop")
    if trip and stop_id:
        selected_stop = get_object_or_404(TripStop, pk=stop_id, trip=trip)

    q = (request.GET.get("q") or "").strip()
    activity_type = (request.GET.get("type") or "").strip()

    activities = Activity.objects.select_related("city")
    if q:
        activities = activities.filter(
            name__icontains=q
        ) | Activity.objects.filter(
            description__icontains=q
        )
    if activity_type:
        activities = activities.filter(activity_type=activity_type)

    return render(
        request,
        "pages/activity_search.html",
        {
            "page_title": "Discover activities — GlobeTrotter",
            "active": "activities",
            "activities": activities.distinct().order_by("city__name", "name"),
            "trip": trip,
            "selected_stop": selected_stop,
            "activity_types": Activity.ACTIVITY_TYPES,
            "stops": trip.stops.select_related("city").all() if trip else [],
        },
    )


@login_required
def calendar_view(request):
    trip = _owned_trip(request, request.GET.get("trip"))
    if not trip:
        return redirect("create_trip")
    stops, activities, _, _ = _trip_context(trip)
    events = [
        a for a in activities if a.date
    ]
    return render(
        request,
        "pages/calendar.html",
        {
            "page_title": f"{trip.name} — Calendar",
            "active": "calendar",
            "trip": trip,
            "stops": stops,
            "events": events,
        },
    )
