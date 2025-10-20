from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
import random, json, datetime



# --------------------- INDEX ---------------------
def index(request):
    # messages.success(request, random.randint(100,200))
    return render(request, "index.html")


# --------------------- LOGIN ---------------------
@never_cache
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard_home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# --------------------- LOGOUT ---------------------
def user_logout(request):
    logout(request)
    return redirect('login')


# --------------------- HOME (Protected) ---------------------
@never_cache
@login_required
def home(request):
    return render(request, "home.html")




def register(request):
    return render(request, "register.html")




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

# You can use a simple session to store OTP temporarily
def verify_email(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()

        # if not email.endswith("@rguktrkv.ac.in"):
        #     messages.error(request, "Please use your college email address.")
        #     return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered. Try logging in.")
            return redirect("register")

        # Generate OTP
        otp = get_random_string(length=6, allowed_chars='0123456789')

        # Save OTP in session for verification later
        request.session['otp'] = otp
        request.session['email'] = email

        # Send OTP via email
        send_mail(
            subject="Your SecondLove Email Verification Code",
            message=f"Your OTP is {otp}. It is valid for 5 minutes.",
            from_email="thriftNshare@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        # messages.success(request, "OTP sent! Check your email inbox.")
        return redirect("verify_otp")  # Next step (you can create verify_otp.html)

    return render(request, "register.html")





from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

# def verify_otp(request):
#     if request.method == "POST":
#         entered_otp = request.POST.get("otp").strip()
#         saved_otp = request.session.get("otp")
#         email = request.session.get("email")

#         if not saved_otp or not email:
#             messages.error(request, "Session expired. Please request a new OTP.")
#             return redirect("verify_email")

#         if entered_otp == saved_otp:
#             # ✅ OTP is correct
#             messages.success(request, "OTP verified successfully!")
            
#             # Remove OTP from session for security
#             del request.session['otp']

#             # Redirect to password creation page (next step)
#             return redirect("create_password")  
#         else:
#             messages.error(request, "Invalid OTP. Please try again.")
#             return redirect("verify_otp")

#     return render(request, "verify_otp.html")




def verify_otp(request):
    email = request.session.get('email')  # assuming you saved email in session
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        if entered_otp == saved_otp:
            messages.success(request, 'OTP verified successfully!')
            return redirect('password')  # your next page
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')
    return render(request, 'verify_otp.html', {'email': email})

def resend_otp(request):
    email = request.session.get('email')
    if email:
        new_otp = str(random.randint(100000, 999999))
        request.session['otp'] = new_otp
        # send OTP via email function here
        messages.success(request, f'New OTP sent to {email}')
        send_mail(
            subject="Your SecondLove Email Verification Code",
            message=f"Your new OTP is {new_otp}. It is valid for 5 minutes.",
            from_email="thriftNshare@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )
    else:
        messages.error(request, 'No email found. Please start the process again.')
    return redirect('verify_otp')




from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def create_password(request):
    """
    Create a new user after email verification with name, email, and password.
    """
    # Get user info from session (after OTP verification)
  
    email = request.session.get('email')
    user_id = email.split('@')[0]


    if not email:
        messages.error(request, "Session expired. Please verify your email again.")
        return redirect('verify_email')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        # elif len(password) < 8:
        #     messages.error(request, "Password must be at least 8 characters long.")
        else:
            # Create new user
            user = User.objects.create_user(
                email=email,
                username=user_id,
                password=password  # set_password handled automatically
            )
            user.save()

            # Clear session
            request.session.pop('verified_email', None)
            request.session.pop('verified_name', None)

            messages.success(request, "Account created successfully!")
            return redirect('dashboard_home')  # Redirect to dashboard/home

    return render(request, 'create_password.html')
