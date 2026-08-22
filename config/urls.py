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
    path('trip/<int:trip_id>/builder/', trips_views.builder_view, name='builder'),
    path('trip/<int:trip_id>/itinerary/', trips_views.itinerary_view, name='itinerary'),
    path('discover/cities/', views.city_search, name='cities'),
    path('discover/activities/', views.activity_search, name='activities'),
    path('trip/<int:trip_id>/budget/', views.budget, name='budget'),
    path('trip/<int:trip_id>/calendar/', views.calendar_view, name='calendar'),
    path('share/<int:trip_id>/sample-trip/', views.public_itinerary, name='public_itinerary'),
    path('profile/', account_views.profile_view, name='profile'),
    path('analytics/', views.admin_dashboard, name='analytics'),
]

# Explicit local static serving keeps the frontend independently runnable during development.
if settings.FRONTEND_ONLY or settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=BASE_DIR / 'static')
