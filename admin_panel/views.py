from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from destinations.models import City
from activities.models import Activity
from trips.models import Trip

from django.contrib.auth import logout
from django.shortcuts import redirect




def dashboard(request):

    context = {
        "total_users": User.objects.count(),
        "total_trips": Trip.objects.count(),
        "total_cities": City.objects.count(),
        "total_activities": Activity.objects.count(),

        "recent_users": User.objects.order_by("-date_joined")[:5],

        "popular_cities": City.objects.order_by("-popularity")[:5],

        "popular_activities": Activity.objects.select_related(
            "city"
        )[:5],
    }

    return render(
        request,
        "admin_panel/dashboard.html",
        context
    )


# =========================================================
# USERS
# =========================================================

def users(request):

    search = request.GET.get("search", "").strip()

    user_list = User.objects.all().order_by("-date_joined")

    if search:

        user_list = user_list.filter(
            username__icontains=search
        ) | user_list.filter(
            email__icontains=search
        )

    context = {
        "users": user_list,
        "search": search,
    }

    return render(
        request,
        "admin_panel/users.html",
        context
    )


def user_detail(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id
    )

    user_trips = Trip.objects.filter(
        user=user
    ).order_by("-start_date")

    context = {
        "user": user,
        "user_trips": user_trips,
    }

    return render(
        request,
        "admin_panel/user_detail.html",
        context
    )


def delete_user(request, user_id):

    if request.method == "POST":

        user = get_object_or_404(
            User,
            id=user_id
        )

        user.delete()

        messages.success(
            request,
            "User deleted successfully."
        )

    return redirect("admin_panel:users")

def users(request):
    search = request.GET.get("search", "").strip()

    user_list = User.objects.all().order_by("-date_joined")

    if search:
        user_list = user_list.filter(
            username__icontains=search
        ) | user_list.filter(
            email__icontains=search
        )

    context = {
        "users": user_list,
        "search": search,
    }

    return render(request, "admin_panel/users.html", context)


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)

    user_trips = Trip.objects.filter(
        user=user
    ).order_by("-start_date")

    return render(
        request,
        "admin_panel/user_detail.html",
        {
            "user": user,
            "user_trips": user_trips,
        }
    )


def delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)

        # Admin ko accidentally delete hone se bachao
        if user.is_superuser:
            messages.error(
                request,
                "Superuser cannot be deleted from this panel."
            )
            return redirect("admin_panel:users")

        user.delete()

        messages.success(
            request,
            "User deleted successfully."
        )

    return redirect("admin_panel:users")

# =========================================================
# CITIES
# =========================================================

def cities(request):

    search = request.GET.get("search", "").strip()
    sort = request.GET.get("sort", "popularity")

    city_list = City.objects.all()

    if search:
        city_list = city_list.filter(
            name__icontains=search
        ) | city_list.filter(
            country__icontains=search
        ) | city_list.filter(
            region__icontains=search
        )

    if sort == "name":
        city_list = city_list.order_by("name")

    elif sort == "cost":
        city_list = city_list.order_by("-cost_index")

    else:
        city_list = city_list.order_by("-popularity")

    context = {
        "cities": city_list,
        "search": search,
        "sort": sort,
        "total_cities": City.objects.count(),
    }

    return render(
        request,
        "admin_panel/cities.html",
        context
    )


def city_create(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        country = request.POST.get("country", "").strip()
        region = request.POST.get("region", "").strip()
        description = request.POST.get("description", "").strip()
        cost_index = request.POST.get("cost_index") or 0
        popularity = request.POST.get("popularity") or 0

        if not name or not country:
            messages.error(
                request,
                "City name and country are required."
            )

            return redirect("admin_panel:city_create")

        City.objects.create(
            name=name,
            country=country,
            region=region,
            description=description,
            cost_index=cost_index,
            popularity=popularity,
        )

        messages.success(
            request,
            f"{name} added successfully."
        )

        return redirect("admin_panel:cities")

    return render(
        request,
        "admin_panel/city_form.html",
        {
            "page_title": "Add City",
            "button_text": "Create City",
        }
    )


def city_edit(request, city_id):

    city = get_object_or_404(
        City,
        id=city_id
    )

    if request.method == "POST":

        city.name = request.POST.get(
            "name", ""
        ).strip()

        city.country = request.POST.get(
            "country", ""
        ).strip()

        city.region = request.POST.get(
            "region", ""
        ).strip()

        city.description = request.POST.get(
            "description", ""
        ).strip()

        city.cost_index = request.POST.get(
            "cost_index"
        ) or 0

        city.popularity = request.POST.get(
            "popularity"
        ) or 0

        city.save()

        messages.success(
            request,
            f"{city.name} updated successfully."
        )

        return redirect(
            "admin_panel:cities"
        )

    return render(
        request,
        "admin_panel/city_form.html",
        {
            "city": city,
            "page_title": "Edit City",
            "button_text": "Save Changes",
        }
    )


def city_delete(request, city_id):

    city = get_object_or_404(
        City,
        id=city_id
    )

    if request.method == "POST":

        city_name = city.name

        city.delete()

        messages.success(
            request,
            f"{city_name} deleted successfully."
        )

    return redirect(
        "admin_panel:cities"
    )

# =========================================================
# ACTIVITIES
# =========================================================

def activities(request):

    search = request.GET.get("search", "").strip()
    city_id = request.GET.get("city", "").strip()
    activity_type = request.GET.get("type", "").strip()

    activity_list = Activity.objects.select_related("city").all()

    # Search
    if search:
        activity_list = activity_list.filter(
            name__icontains=search
        )

    # City filter
    if city_id:
        activity_list = activity_list.filter(
            city_id=city_id
        )

    # Activity type filter
    if activity_type:
        activity_list = activity_list.filter(
            activity_type=activity_type
        )

    cities_list = City.objects.all().order_by("name")

    activity_types = (
        Activity.objects
        .values_list("activity_type", flat=True)
        .distinct()
        .order_by("activity_type")
    )

    context = {
        "activities": activity_list,
        "cities": cities_list,
        "activity_types": activity_types,
        "search": search,
        "selected_city": city_id,
        "selected_type": activity_type,
        "total_activities": Activity.objects.count(),
    }

    return render(
        request,
        "admin_panel/activities.html",
        context
    )


def activity_create(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        city_id = request.POST.get("city")
        description = request.POST.get("description", "").strip()
        activity_type = request.POST.get(
            "activity_type",
            ""
        ).strip()

        duration = request.POST.get(
            "duration",
            ""
        ).strip()

        estimated_cost = request.POST.get(
            "estimated_cost"
        ) or 0


        if not name or not city_id:

            messages.error(
                request,
                "Activity name and city are required."
            )

            return redirect(
                "admin_panel:activity_create"
            )


        city = get_object_or_404(
            City,
            id=city_id
        )


        Activity.objects.create(

            name=name,

            city=city,

            description=description,

            activity_type=activity_type,

            duration=duration,

            estimated_cost=estimated_cost,

        )


        messages.success(
            request,
            f"{name} added successfully."
        )


        return redirect(
            "admin_panel:activities"
        )


    return render(
        request,
        "admin_panel/activity_form.html",
        {
            "page_title": "Add Activity",
            "button_text": "Create Activity",
            "cities": City.objects.all().order_by("name"),
        }
    )


def activity_edit(request, activity_id):

    activity = get_object_or_404(
        Activity,
        id=activity_id
    )


    if request.method == "POST":

        activity.name = request.POST.get(
            "name",
            ""
        ).strip()

        activity.city_id = request.POST.get(
            "city"
        )

        activity.description = request.POST.get(
            "description",
            ""
        ).strip()

        activity.activity_type = request.POST.get(
            "activity_type",
            ""
        ).strip()

        activity.duration = request.POST.get(
            "duration",
            ""
        ).strip()

        activity.estimated_cost = request.POST.get(
            "estimated_cost"
        ) or 0

        activity.save()


        messages.success(
            request,
            f"{activity.name} updated successfully."
        )


        return redirect(
            "admin_panel:activities"
        )


    return render(
        request,
        "admin_panel/activity_form.html",
        {
            "activity": activity,
            "page_title": "Edit Activity",
            "button_text": "Save Changes",
            "cities": City.objects.all().order_by("name"),
        }
    )


def activity_delete(request, activity_id):

    activity = get_object_or_404(
        Activity,
        id=activity_id
    )


    if request.method == "POST":

        activity_name = activity.name

        activity.delete()

        messages.success(
            request,
            f"{activity_name} deleted successfully."
        )


    return redirect(
        "admin_panel:activities"
    )

def analytics(request):

    total_users = User.objects.count()
    total_trips = Trip.objects.count()
    total_cities = City.objects.count()
    total_activities = Activity.objects.count()

    user_growth = (
        User.objects
        .annotate(month=TruncMonth("date_joined"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    trip_growth = (
        Trip.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    popular_cities = City.objects.order_by(
        "-popularity"
    )[:5]

    popular_activities = Activity.objects.order_by(
        "-estimated_cost"
    )[:5]

    context = {
        "total_users": total_users,
        "total_trips": total_trips,
        "total_cities": total_cities,
        "total_activities": total_activities,

        "user_growth": list(user_growth),
        "trip_growth": list(trip_growth),

        "popular_cities": popular_cities,
        "popular_activities": popular_activities,
    }

    return render(
        request,
        "admin_panel/analytics.html",
        context
    )

def settings_page(request):

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name", ""
        ).strip()

        last_name = request.POST.get(
            "last_name", ""
        ).strip()

        email = request.POST.get(
            "email", ""
        ).strip()

        user = request.user

        if user.is_authenticated:

            user.first_name = first_name
            user.last_name = last_name
            user.email = email

            user.save()

            messages.success(
                request,
                "Settings saved successfully."
            )

        return redirect(
            "admin_panel:settings"
        )

    return render(
        request,
        "admin_panel/settings.html"
    )

def admin_logout(request):
    logout(request)
    return redirect("login")