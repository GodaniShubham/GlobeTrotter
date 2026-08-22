from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from accounts import views as account_views
from config import views
from trips import views as trips_views


BASE_DIR = Path(settings.BASE_DIR)


urlpatterns = [
    path("admin/", admin.site.urls),

    # Admin panel
    path("admin-panel/", include("admin_panel.urls")),

    # Main website
    path("", views.landing, name="home"),
    path("login/", account_views.login_view, name="login"),
    path("signup/", account_views.signup_view, name="signup"),
    path("logout/", account_views.logout_view, name="logout"),

    path("dashboard/", trips_views.dashboard_view, name="dashboard"),
    path("trips/new/", trips_views.create_trip_view, name="create_trip"),
    path("trips/", trips_views.trips_view, name="trips"),

    # Trip builder
    path("trip/builder/", trips_views.builder_view, name="builder"),
    path(
        "trip/<int:trip_id>/builder/",
        trips_views.builder_view,
        name="trip_builder",
    ),

    # Trip stops
    path(
        "trip/stops/add/",
        trips_views.add_stop,
        name="trip_stop_add",
    ),
    path(
        "trip/stops/<int:pk>/update/",
        trips_views.update_stop,
        name="trip_stop_update",
    ),
    path(
        "trip/stops/reorder/",
        trips_views.reorder_stops,
        name="trip_stop_reorder",
    ),
    path(
        "trip/stops/<int:pk>/delete/",
        trips_views.delete_stop,
        name="trip_stop_delete",
    ),

    # Trip activities
    path(
        "trip/activities/add/",
        trips_views.add_activity,
        name="trip_activity_add",
    ),
    path(
        "trip/activities/<int:pk>/update/",
        trips_views.update_activity,
        name="trip_activity_update",
    ),
    path(
        "trip/activities/<int:pk>/delete/",
        trips_views.delete_activity,
        name="trip_activity_delete",
    ),

    # Itinerary
    path("trip/itinerary/", trips_views.itinerary_view, name="itinerary"),
    path(
        "trip/<int:trip_id>/itinerary/",
        trips_views.itinerary_view,
        name="trip_itinerary",
    ),

    # Discovery
    path(
        "discover/cities/",
        trips_views.city_search_view,
        name="cities",
    ),
    path(
        "discover/activities/",
        trips_views.activity_search_view,
        name="activities",
    ),

    # Budget / calendar / public itinerary
    path("trip/budget/", views.budget, name="budget"),
    path(
        "trip/<int:trip_id>/budget/",
        views.budget,
        name="trip_budget",
    ),
    path(
        "trip/calendar/",
        trips_views.calendar_view,
        name="calendar",
    ),
    path(
        "trip/<int:trip_id>/calendar/",
        trips_views.calendar_view,
        name="trip_calendar",
    ),
    path(
        "share/sample-trip/",
        views.public_itinerary,
        name="public_itinerary",
    ),
    path(
        "share/<int:trip_id>/sample-trip/",
        views.public_itinerary,
        name="trip_public_itinerary",
    ),

    # Authentication / password reset
    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password",
    ),
    path(
        "forgot-password/otp/",
        views.otp_verify,
        name="otp_verify",
    ),
    path(
        "forgot-password/reset/",
        views.reset_password,
        name="reset_password",
    ),

    # Community
    path("community/", views.community, name="community"),

    path("profile/", account_views.profile_view, name="profile"),
    path("analytics/", views.admin_dashboard, name="analytics"),
]


if settings.FRONTEND_ONLY or settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=BASE_DIR / "static",
    )