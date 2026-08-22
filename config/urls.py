from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from config import views
from pathlib import Path

BASE_DIR = Path(settings.BASE_DIR)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('trips/new/', views.create_trip, name='create_trip'),
    path('trips/', views.trips, name='trips'),
    path('trip/builder/', views.builder, name='builder'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path('trip/itinerary/', views.itinerary, name='itinerary'),
    path('discover/cities/', views.city_search, name='cities'),
    path('discover/activities/', views.activity_search, name='activities'),
    path('trip/budget/', views.budget, name='budget'),
    path('trip/calendar/', views.calendar_view, name='calendar'),
    path('share/sample-trip/', views.public_itinerary, name='public_itinerary'),
    path('profile/', views.profile, name='profile'),
    path('analytics/', views.admin_dashboard, name='analytics'),
]

# Explicit local static serving keeps the frontend independently runnable during development.
if settings.FRONTEND_ONLY or settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=BASE_DIR / 'static')
