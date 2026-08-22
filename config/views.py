from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random

def page(template, title="GlobeTrotter", **context):
    context.setdefault("page_title", title)
    return render(None, template, context)

def _render(request, template, title, **context):
    context.setdefault("page_title", title)
    return render(request, template, context)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email and User.objects.filter(email=email).exists():
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            
            try:
                html_msg = render_to_string('emails/otp_email.html', {'otp': otp})
                send_mail(
                    subject='Your GlobeTrotter Password Reset OTP',
                    message=f'Hi there,\n\nWe received a request to reset your password.\nYour One-Time Password (OTP) is: {otp}\n\nIf you did not request this, please ignore this email.\n\nThe GlobeTrotter Team',
                    from_email='godanishubham30@gmail.com',
                    recipient_list=[email],
                    html_message=html_msg,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error sending forgot password email: {e}")
                
            return redirect('otp_verify')
        else:
            messages.success(request, 'If your email exists in our system, you will receive a reset link shortly.')
        
    return render(request, "pages/forgot_password.html")

def otp_verify(request):
    # Ensure user has started the flow
    if 'reset_email' not in request.session or 'reset_otp' not in request.session:
        return redirect('forgot_password')
        
    email = request.session['reset_email']
    
    if request.method == 'POST':
        if 'resend' in request.POST:
            # Resend OTP
            otp = str(random.randint(100000, 999999))
            request.session['reset_otp'] = otp
            
            try:
                html_msg = render_to_string('emails/otp_email.html', {'otp': otp})
                send_mail(
                    subject='Your GlobeTrotter Password Reset OTP (Resent)',
                    message=f'Hi there,\n\nHere is your new One-Time Password (OTP): {otp}\n\nIf you did not request this, please ignore this email.\n\nThe GlobeTrotter Team',
                    from_email='godanishubham30@gmail.com',
                    recipient_list=[email],
                    html_message=html_msg,
                    fail_silently=True,
                )
                messages.success(request, 'A new OTP has been sent to your email.')
            except Exception as e:
                print(f"Error resending OTP email: {e}")
                
        else:
            # Verify OTP
            entered_otp = request.POST.get('otp', '').strip()
            if entered_otp == request.session['reset_otp']:
                request.session['otp_verified'] = True
                return redirect('reset_password')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                
    return render(request, 'pages/otp_verify.html', {'email': email})

def reset_password(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
        
    email = request.session.get('reset_email')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            # Update password
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            
            # Clear session
            request.session.pop('reset_email', None)
            request.session.pop('reset_otp', None)
            request.session.pop('otp_verified', None)
            
            messages.success(request, 'Your password has been successfully reset. You can now log in.')
            return redirect('login')
            
    return render(request, 'pages/reset_password.html', {'email': email})
def community(request):
    return render(request, "pages/community.html")
def landing(request):
    from trips.models import Trip
    public_trip = Trip.objects.filter(is_public=True).first()
    if not public_trip:
        public_trip = Trip.objects.first() # fallback to any trip for the demo
        
    context = {
        'public_trip': public_trip
    }
    return render(request, "pages/landing.html", context)


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


@login_required
def budget(request, trip_id):
    from trips.models import Trip
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    stops = trip.stops.prefetch_related('itinerary_activities').all()
    
    total_cost = 0
    cat_totals = {'Activities': 0, 'Transport': 0, 'Accommodation': 0, 'Meals': 0, 'Other': 0}
    
    for stop in stops:
        for it_act in stop.itinerary_activities.all():
            cost = float(it_act.custom_cost or it_act.activity.estimated_cost or 0)
            total_cost += cost
            cat = it_act.activity.activity_type
            if cat in cat_totals:
                cat_totals[cat] += cost
            else:
                cat_totals['Other'] += cost
                
    context = {
        'page_title': f'{trip.name} Budget — GlobeTrotter',
        'active': 'budget',
        'trip': trip,
        'total_cost': total_cost,
        'cat_totals': cat_totals
    }
    return render(request, "pages/budget.html", context)


@login_required
def calendar_view(request, trip_id):
    from trips.models import Trip
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    context = {
        'page_title': f'{trip.name} Calendar — GlobeTrotter',
        'active': 'calendar',
        'trip': trip
    }
    return render(request, "pages/calendar.html", context)


def public_itinerary(request, trip_id):
    from trips.models import Trip
    trip = get_object_or_404(Trip, id=trip_id, is_public=True)
    stops = trip.stops.prefetch_related('itinerary_activities__activity').all()
    context = {
        'page_title': f'{trip.name} — GlobeTrotter',
        'trip': trip,
        'stops': stops
    }
    return render(request, "pages/public_itinerary.html", context)


def profile(request):
    return _render(request, "pages/profile.html", "Profile & settings — GlobeTrotter", active="profile")


def admin_dashboard(request):
    return _render(request, "pages/admin_dashboard.html", "Analytics — GlobeTrotter", active="admin")
