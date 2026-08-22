from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to find user by email to get username
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            
    context = {
        'page_title': 'Sign in — GlobeTrotter',
        'auth_mode': 'login'
    }
    return render(request, "pages/auth.html", context)

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            # Create the user. Use email as username since we don't collect a username.
            username = email.split('@')[0]
            # Ensure uniqueness
            original_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
                
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Send welcome email
            try:
                html_msg = render_to_string('emails/welcome_email.html', {'first_name': first_name or username})
                send_mail(
                    subject='Welcome to GlobeTrotter!',
                    message=f'Hi {first_name or username},\n\nWelcome to GlobeTrotter! Your workspace is ready for your next big journey.\n\nHappy travels,\nThe GlobeTrotter Team',
                    from_email='godanishubham30@gmail.com',
                    recipient_list=[email],
                    html_message=html_msg,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Error sending welcome email: {e}")

            auth_login(request, user)
            return redirect('dashboard')
            
    context = {
        'page_title': 'Create account — GlobeTrotter',
        'auth_mode': 'signup'
    }
    return render(request, "pages/auth.html", context)

def logout_view(request):
    auth_logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        currency = request.POST.get('currency')
        
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()
        
        if hasattr(request.user, 'userprofile') and currency:
            request.user.userprofile.currency = currency
            request.user.userprofile.save()
            
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
        
    context = {
        'page_title': 'Profile & settings — GlobeTrotter',
        'active': 'profile'
    }
    return render(request, "pages/profile.html", context)
