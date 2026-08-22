from pathlib import Path
from datetime import datetime

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import include, path
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts import views as account_views
from activities.models import Activity
from community import views as community_views
from config import views
from destinations.models import City
from trips import views as trips_views
from trips.models import Trip, TripStop


BASE_DIR = Path(settings.BASE_DIR)


def _request_trip_id(request):
    """Resolve a trip id from the query string, with the user's latest trip as fallback."""
    raw = request.GET.get("trip_id") or request.GET.get("trip")
    if raw and str(raw).isdigit():
        return int(raw)

    if getattr(request.user, "is_authenticated", False):
        trip = Trip.objects.filter(user=request.user).order_by("-created_at").first()
        return trip.pk if trip else None
    return None


@login_required
def budget_compat(request):
    """Compatibility wrapper for the older /trip/budget/?trip=<id> route."""
    trip_id = _request_trip_id(request)
    if not trip_id:
        return redirect("create_trip")
    return views.budget(request, trip_id)


@login_required
def itinerary_compat(request):
    """Compatibility wrapper for old and new itinerary signatures."""
    trip_id = _request_trip_id(request)
    if not trip_id:
        return redirect("create_trip")
    try:
        return trips_views.itinerary_view(request, trip_id)
    except TypeError as exc:
        if "positional argument" in str(exc):
            return trips_views.itinerary_view(request)
        raise


@login_required
def calendar_compat(request):
    """Compatibility wrapper for old and new calendar signatures."""
    trip_id = _request_trip_id(request)
    if not trip_id:
        return redirect("create_trip")
    try:
        return trips_views.calendar_view(request, trip_id)
    except TypeError as exc:
        if "positional argument" in str(exc):
            return trips_views.calendar_view(request)
        raise


def public_itinerary_compat(request, trip_id=None):
    """Keep shared-itinerary URLs compatible across the merged branches."""
    resolved = trip_id or _request_trip_id(request)
    if not resolved:
        return redirect("home")
    try:
        return views.public_itinerary(request, resolved)
    except TypeError as exc:
        if "positional argument" in str(exc):
            return views.public_itinerary(request)
        raise


@login_required
@require_POST
def add_stop_manual_compat(request):
    """Manual planner endpoint: add a city with exact arrival/departure dates."""
    raw_trip = request.POST.get("trip_id")
    trip = get_object_or_404(Trip, pk=raw_trip, user=request.user)
    city = get_object_or_404(City, pk=request.POST.get("city_id"))

    if TripStop.objects.filter(trip=trip, city=city).exists():
        return JsonResponse(
            {"ok": False, "message": f"{city.name} is already in this trip."},
            status=400,
        )

    def parse_date(value):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            return None

    arrival = parse_date(request.POST.get("arrival_date")) or trip.start_date
    departure = parse_date(request.POST.get("departure_date")) or arrival

    if arrival < trip.start_date or departure > trip.end_date:
        return JsonResponse(
            {"ok": False, "message": "Stop dates must stay inside the trip dates."},
            status=400,
        )
    if departure < arrival:
        return JsonResponse(
            {"ok": False, "message": "Departure must be on or after arrival."},
            status=400,
        )

    order = (
        TripStop.objects.filter(trip=trip)
        .aggregate(max_order=Max("order"))
        .get("max_order")
        or 0
    ) + 1

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
                "arrival": arrival.isoformat(),
                "departure": departure.isoformat(),
            },
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),

    # Main admin panel
    path("admin-panel/", include("admin_panel.urls")),

    # Main website
    path("", views.landing, name="home"),
    path("login/", account_views.login_view, name="login"),
    path("signup/", account_views.signup_view, name="signup"),
    path("logout/", account_views.logout_view, name="logout"),

    path("dashboard/", trips_views.dashboard_view, name="dashboard"),
    path("trips/new/", trips_views.create_trip_view, name="create_trip"),
    path("trips/", trips_views.trips_view, name="trips"),

    # Manual builder
    path("trip/builder/", trips_views.builder_view, name="builder"),
    path("trip/<int:trip_id>/builder/", trips_views.builder_view, name="trip_builder"),

    # Manual stop management
    path("trip/stops/add/", trips_views.add_stop, name="trip_stop_add"),
    path("trip/stops/add-manual/", add_stop_manual_compat, name="trip_stop_manual_add"),
    path("trip/stops/<int:pk>/update/", trips_views.update_stop, name="trip_stop_update"),
    path("trip/stops/reorder/", trips_views.reorder_stops, name="trip_stop_reorder"),
    path("trip/stops/<int:pk>/delete/", trips_views.delete_stop, name="trip_stop_delete"),

    # Activity management
    path("trip/activities/add/", trips_views.add_activity, name="trip_activity_add"),
    path("trip/activities/<int:pk>/update/", trips_views.update_activity, name="trip_activity_update"),
    path("trip/activities/<int:pk>/delete/", trips_views.delete_activity, name="trip_activity_delete"),

    # Itinerary + calendar compatibility
    path("trip/itinerary/", itinerary_compat, name="itinerary"),
    path("trip/<int:trip_id>/itinerary/", itinerary_compat, name="trip_itinerary"),

    # Discovery
    path("discover/cities/", trips_views.city_search_view, name="cities"),
    path("discover/activities/", trips_views.activity_search_view, name="activities"),

    # Budget/calendar/public sharing compatibility
    path("trip/budget/", budget_compat, name="budget"),
    path("trip/<int:trip_id>/budget/", views.budget, name="trip_budget"),
    path("trip/calendar/", calendar_compat, name="calendar"),
    path("trip/<int:trip_id>/calendar/", calendar_compat, name="trip_calendar"),
    path("share/sample-trip/", public_itinerary_compat, name="public_itinerary"),
    path("share/<int:trip_id>/sample-trip/", public_itinerary_compat, name="trip_public_itinerary"),

    # Authentication / recovery
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("forgot-password/otp/", views.otp_verify, name="otp_verify"),
    path("forgot-password/reset/", views.reset_password, name="reset_password"),

    # Community
    path("community/", community_views.feed, name="community"),
    path("community/new/", community_views.create_post, name="community_new"),
    path("community/saved/", community_views.saved_posts, name="community_saved"),
    path("community/post/<int:pk>/", community_views.post_detail, name="community_post"),
    path("community/post/<int:pk>/reply/", community_views.reply_to_post, name="community_reply"),
    path("community/post/<int:pk>/like/", community_views.toggle_like, name="community_like"),
    path("community/post/<int:pk>/save/", community_views.toggle_save, name="community_save"),
    path("community/reply/<int:pk>/like/", community_views.toggle_reply_like, name="community_reply_like"),
    path("community/reply/<int:pk>/delete/", community_views.delete_reply, name="community_reply_delete"),
    path("community/post/<int:pk>/report/", community_views.report_post, name="community_report"),
    path("community/post/<int:pk>/delete/", community_views.delete_post, name="community_delete"),
    path("community/post/<int:pk>/share/", community_views.record_share, name="community_share"),
    path("community/post/<int:pk>/updates/", community_views.post_updates, name="community_updates"),
    path("community/notifications/", community_views.notifications, name="community_notifications"),
    path("community/notifications/read/", community_views.mark_notifications_read, name="community_notifications_read"),

    path("profile/", account_views.profile_view, name="profile"),
    path("analytics/", views.admin_dashboard, name="analytics"),
]


if settings.FRONTEND_ONLY or settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=BASE_DIR / "static",
    )
