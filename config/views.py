from django.shortcuts import render


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
    return _render(request, "pages/landing.html", "GlobeTrotter — Plan travel beautifully", public=True)


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


def budget(request):
    return _render(request, "pages/budget.html", "Trip budget — GlobeTrotter", active="budget")


def calendar_view(request):
    return _render(request, "pages/calendar.html", "Trip calendar — GlobeTrotter", active="calendar")


def public_itinerary(request):
    return _render(request, "pages/public_itinerary.html", "Shared itinerary — GlobeTrotter", public=True)


def profile(request):
    return _render(request, "pages/profile.html", "Profile & settings — GlobeTrotter", active="profile")


def admin_dashboard(request):
    return _render(request, "pages/admin_dashboard.html", "Analytics — GlobeTrotter", active="admin")
