from django import forms
from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone

from authtools.models import User
from authtools.forms import UserCreationForm
import json
from .models import Profile
from .helper import *

from niser_app.local_settings import *
from .daily_tasks import My_Send_Email
from .forms import ProfileEditForm
from django.views.generic.edit import UpdateView
from django.core.files.images import ImageFile


# def error404(request, exception):
#     return render(request, 'main/404.htm', {'exp': exception}, status=404)


# def error500(request, exception):
#     return render(request, 'main/500.htm', {'exp': exception}, status=500)





class EmailForm(forms.Form):
    email = forms.EmailField()





def home(request):
    return render(request, 'my_user/index.html')

def signup(request):
    if request.user is not None and request.user.is_authenticated:
        error_message = "You are already logged in! No need to signup. If you still want to signup, " 
        error_message += "please either logout first or open the site in an incognito window"
        messages.error(request, error_message)
        return render(request, "my_user/index.html")
    if request.method == 'POST':
        # print(f"\n{dict(request.POST)['email'][0] = }, {type(dict(request.POST)['email'][0]) = }\n")
        emailForm = EmailForm(request.POST)
        
        if not dict(request.POST)['email'][0].endswith("@niser.ac.in"):
            messages.error(request, "Please use your NISER email address")
            return redirect('signup')
        if emailForm.is_valid():
            try:
                u = User.objects.get(email=emailForm.cleaned_data['email'])
            except User.DoesNotExist:
                u = None
            if u and not u.is_active:
                u.delete()  # Delete the user if it exists but is not active
                # This case arises when the user fills the form twice and the first time the email was not verified
                # So we choose to forget that the user had filled the form once before.

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.is_valid()
            user = form.save(commit=False)
            # we get an instance of an User created from the form. We don't yet save the user to the database
            user.is_active = False  # We set the user to inactive so that we can set it to active only after verifying the email address
            user.save()  # Now we save the user
            
            uvid = genVID(user.email)  # Generate a unique verification ID for the email address
            
            profile = Profile(
                user = user,
                vid = uvid,
                ip = getIP(request),
                joined = timezone.now(),
                # dp = ,
                # data = "",  # IDK
                # upd = False,  # IDK
                karma = 0
            )
            profile.save()

            # Send Verification email
            My_Send_Email(
                to=[user.email],
                subject='Verification of email address - NISER Archive',
                message=render_to_string('my_user/verify.txt', {'user': user, 'vid': uvid, 'dmn': DOMAIN}),
            ).start()
            # print(f"\n\nVerification email has been sent. This is the verification link: {DOMAIN}/auth/verify/{user.pk}/{uvid}\n")

            messages.success(request, "Thank you for signing up. We have sent you a verification email.")
            return redirect("home")
            return render(request, 'my_user/index.html')
    else:
        form = UserCreationForm()
    return render(request, 'my_user/signup.html', {'form': form})

def verify(request, uid, vid):
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user is not None and user.profile.vid == vid:
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your email has been verified. Welcome to NISER Archive!')
        
        # Send Welcome email
        # print(f"\n\nWelcome email has been sent.")
        My_Send_Email(
            to=[user.email],
            subject=f'Welcome {user.name}!',
            message=render_to_string('my_user/welcome.txt', {'user': user, 'dmn': DOMAIN}),
        ).start()
        
        return render(request, 'my_user/index.html')
    else:
        return HttpResponse('Activation link is invalid!')

def login_redirect(request):
    messages.success(request, "Logged In")
    return redirect("home")

def logout_view(request):
    if request.user is not None and request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully!")
    else:
        messages.warning(request, "Are you a Serial Logout-er? Sorry to hurt your feelings, but to log out, you need to login first!")
    return redirect("home")
    # return render(request, 'my_user/index.html')

def profile(request):
    if request.user is not None and request.user.is_authenticated:
        return render(request, 'my_user/profile.html', {'user': request.user})
    else:
        messages.error(request, "Please login first to view your profile")
        return redirect("home")

def edit_profile(request):
    
    if request.user is None or not request.user.is_authenticated:
        messages.error(request, "Please login first to edit your profile")
        return redirect("/auth/login")

    if request.method == "GET":
        form = ProfileEditForm(initial={
            "dp": request.user.profile.dp,
            "school": request.user.profile.school,
            "batch": request.user.profile.batch,
            "prog": request.user.profile.prog,
            "about": request.user.profile.about,
            "gender": request.user.profile.gender,
        })
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance = request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("/profile")
    return render(request, 'my_user/update_profile.html', {'user': request.user, "form": form})

# API Views
def device_token(request, token):
    # This view is called every time the user opens the app
    # The user tells us his token. We store it in a file.
    # Not necessarily the user have to have an account to 
    # use the app. So any users (irrespective of whether 
    # logged in or not) can (have to) send us their token.
    # THIS TOKEN ONLY HELPS US SEND NOTIFICATION TO THE APP. nothing else.
    # This token probably won't change unless the user does destructive
    # tasks like uninstalls the app, erases the app data etc.

    try:
        with open(NOTIFICATION_TOKEN_FILE) as f:
            tokens = json.load(f)
    except FileNotFoundError:
        tokens = []

    if token not in tokens:  # If token is not already present
        tokens.append(token)
        with open(NOTIFICATION_TOKEN_FILE, 'w') as f:  # If file doesn't exist, it will be created
            json.dump(tokens, f)
    # else:
    #     print(f"Token already present")

    # have to return sth... unimportant... just to make the request successful
    return HttpResponse("OK")