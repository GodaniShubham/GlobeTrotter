from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from config import views
from pathlib import Path
from accounts import views as account_views
from trips import views as trips_views
from community import views as community_views

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
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path('community/', community_views.feed, name='community'),
    path('community/new/', community_views.create_post, name='community_new'),
    path('community/saved/', community_views.saved_posts, name='community_saved'),
    path('community/post/<int:pk>/', community_views.post_detail, name='community_post'),
    path('community/post/<int:pk>/reply/', community_views.reply_to_post, name='community_reply'),
    path('community/post/<int:pk>/like/', community_views.toggle_like, name='community_like'),
    path('community/post/<int:pk>/save/', community_views.toggle_save, name='community_save'),
    path('community/reply/<int:pk>/like/', community_views.toggle_reply_like, name='community_reply_like'),
    path('community/reply/<int:pk>/delete/', community_views.delete_reply, name='community_reply_delete'),
    path('community/notifications/', community_views.notifications, name='community_notifications'),
    path('community/notifications/read/', community_views.mark_notifications_read, name='community_notifications_read'),
    path('community/post/<int:pk>/updates/', community_views.post_updates, name='community_updates'),
    path('community/post/<int:pk>/share/', community_views.record_share, name='community_share'),
    path('community/post/<int:pk>/report/', community_views.report_post, name='community_report'),
    path('community/post/<int:pk>/delete/', community_views.delete_post, name='community_delete'),
    path('trip/itinerary/', trips_views.itinerary_view, name='itinerary'),
    path('discover/cities/', views.city_search, name='cities'),
    path('discover/activities/', views.activity_search, name='activities'),
    path('trip/budget/', views.budget, name='budget'),
    path('trip/calendar/', views.calendar_view, name='calendar'),
    path('share/sample-trip/', views.public_itinerary, name='public_itinerary'),
    path('profile/', account_views.profile_view, name='profile'),
    path('analytics/', views.admin_dashboard, name='analytics'),
]

# Explicit local static serving keeps the frontend independently runnable during development.
if settings.FRONTEND_ONLY or settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=BASE_DIR / 'static')
