from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [

    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),


    # =====================================================
    # USERS
    # =====================================================

    path(
        "users/",
        views.users,
        name="users"
    ),

    path(
        "users/<int:user_id>/",
        views.user_detail,
        name="user_detail"
    ),

    path(
        "users/<int:user_id>/delete/",
        views.delete_user,
        name="delete_user"
    ),


    # =====================================================
    # CITIES
    # =====================================================

    path(
        "cities/",
        views.cities,
        name="cities"
    ),

    path(
        "cities/add/",
        views.city_create,
        name="city_create"
    ),

    path(
        "cities/<int:city_id>/edit/",
        views.city_edit,
        name="city_edit"
    ),

    path(
        "cities/<int:city_id>/delete/",
        views.city_delete,
        name="city_delete"
    ),


    # =====================================================
    # ACTIVITIES
    # =====================================================

    path(
        "activities/",
        views.activities,
        name="activities"
    ),

    path(
        "activities/add/",
        views.activity_create,
        name="activity_create"
    ),

    path(
        "activities/<int:activity_id>/edit/",
        views.activity_edit,
        name="activity_edit"
    ),

    path(
        "activities/<int:activity_id>/delete/",
        views.activity_delete,
        name="activity_delete"
    ),

# =====================================================
# ANALYTICS
# =====================================================

path(
    "analytics/",
    views.analytics,
    name="analytics"
),

# =====================================================
# SETTINGS
# =====================================================

path(
    "settings/",
    views.settings_page,
    name="settings"
),

# =====================================================
# LOGOUT
# =====================================================

path(
    "logout/",
    views.admin_logout,
    name="logout"
),
]