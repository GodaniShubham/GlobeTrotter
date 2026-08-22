from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from config import views
from pathlib import Path
from accounts import views as account_views
from trips import views as trips_views

BASE_DIR = Path(settings.BASE_DIR)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='home'),
    path('login/', account_views.login_view, name='login'),
    path('signup/', account_views.signup_view, name='signup'),
    path('logout/', account_views.logout_view, name='logout'),
    path('dashboard/', trips_views.dashboard_view, name='dashboard'),
    path('trips/new/', trips_views.create_trip_view, name='create_trip'),
    path('trips/', trips_views.trips_view, name='trips'),
    path('trip/builder/', trips_views.builder_view, name='builder'),
    path('trip/stops/add/', trips_views.add_stop, name='trip_stop_add'),
    path('trip/stops/<int:pk>/update/', trips_views.update_stop, name='trip_stop_update'),
    path('trip/stops/reorder/', trips_views.reorder_stops, name='trip_stop_reorder'),
    path('trip/stops/<int:pk>/delete/', trips_views.delete_stop, name='trip_stop_delete'),
    path('trip/activities/add/', trips_views.add_activity, name='trip_activity_add'),
    path('trip/activities/<int:pk>/update/', trips_views.update_activity, name='trip_activity_update'),
    path('trip/activities/<int:pk>/delete/', trips_views.delete_activity, name='trip_activity_delete'),

    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("community/", views.community, name="community"),
    path('trip/itinerary/', trips_views.itinerary_view, name='itinerary'),
    path('discover/cities/', trips_views.city_search_view, name='cities'),
    path('discover/activities/', trips_views.activity_search_view, name='activities'),
    path('trip/budget/', views.budget, name='budget'),
    path('trip/calendar/', trips_views.calendar_view, name='calendar'),
    path('share/sample-trip/', views.public_itinerary, name='public_itinerary'),
    path('profile/', account_views.profile_view, name='profile'),
    path('analytics/', views.admin_dashboard, name='analytics'),
]

# Explicit local static serving keeps the frontend independently runnable during development.
if settings.FRONTEND_ONLY or settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=BASE_DIR / 'static')
