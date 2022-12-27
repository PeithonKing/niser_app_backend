from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

pw_reset_view = auth_views.PasswordResetView.as_view(
    template_name           = 'my_user/password-reset.html',
    email_template_name     = 'my_user/password-reset-email.html',
    subject_template_name   = 'my_user/pw-reset-subj.txt'
)

urlpatterns = [
    path("", views.home, name="home"),
    
    # Signup
    path("signup", views.signup, name="signup"),
    path('auth/verify/<uid>/<vid>/', views.verify, name='verify'),
    
    # Login
    path('auth/login/', auth_views.LoginView.as_view(template_name='my_user/login.html'), name='login'),
    path("accounts/profile/", views.login_redirect, name="login_redirect"),
    
    # Logout
    path('auth/logout/', views.logout_view, name='logout'),
    
    # Password Reset
    path('password_reset/', pw_reset_view, name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='my_user/password-reset-done.html'), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='my_user/new_password.html'), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='my_user/password-reset-complete.html'), name="password_reset_complete"),
    
    # Profile Viewing and tweaking
    path("profile/", views.profile, name="profile"),
    path("edit_profile/" , views.edit_profile, name="edit_profile"),
    
    
    
    
    # API Views
    path("device_token/<token>", views.device_token, name="device_token"),
]