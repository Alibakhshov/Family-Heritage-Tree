import logging
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import escape
from .models import CustomUser
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

# Function to handle user login
def user_login(request):
    try:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('tree/')
        else:
            form = AuthenticationForm()
        return render(request, 'authentication/signIn/signIn.html', {'form': form})
    except Exception as e:
        logger.exception("An error occurred in user_login: %s", str(e))

# Function to handle user logout
def user_logout(request):
    try:
        logout(request)
        return redirect('login')
    except Exception as e:
        logger.exception("An error occurred in user_logout: %s", str(e))

# Function to handle user registration
def user_register(request):
    try:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False 
                user.save()

                # Generate a token for email confirmation
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Construct email verification link
                verification_link = reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})
                confirmation_url = request.build_absolute_uri(verification_link)

                # Send email for verification
                subject = 'Confirm your email address'
                html_message = render_to_string('authentication/signUp/confirm_email.html', {
                    'user': user,
                    'confirmation_url': confirmation_url,
                })
                plain_message = strip_tags(html_message)
                user.email_user(subject, plain_message)

                return redirect('register_confirmation') 
        else:
            form = CustomUserCreationForm()
        return render(request, 'authentication/signUp/signup.html', {'form': form})
    except Exception as e:
        logger.exception("An error occurred in user_register: %s", str(e))

def registration_confirmation(request):
    return render(request, 'authentication/signUp/email_sent.html')

def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    try:
        if user is not None and default_token_generator.check_token(user, token):
            user.email_confirmed = True
            user.is_active = True
            user.save() 
            return render(request, 'authentication/signUp/email_confirmed.html')
        else:
            return render(request, 'authentication/signUp/email_not_confirmed.html')
    except Exception as e:
        logger.exception("An error occurred in confirm_email: %s", str(e))

def password_reset_request(request):
    try:
        if request.method == "POST":
            email = request.POST['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                # Generate a password reset token
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                # Send email with password reset link
                reset_link = request.build_absolute_uri(
                    f'/reset/{uid}/{token}/'
                )
                email_subject = 'Password Reset Request'
                email_body = render_to_string(
                    'authentication/resetPassword/password_reset_email.html',
                    {'reset_link': reset_link}
                )
                # Escape HTML content to display it as text
                escaped_email_body = escape(email_body)

                send_mail(
                    email_subject,
                    '',
                    'raufalibakhshov02@gmail.com',
                    [email],
                    fail_silently=False,
                    html_message=email_body
                )
                return redirect('password_reset_done')
            else:
                messages.error(
                    request,
                    'No user with this email address exists. Please check the email you entered.'
                )
                return render(request, 'authentication/resetPassword/password_reset_request.html')

        return render(request, 'authentication/resetPassword/password_reset_request.html')
    except Exception as e:
        logger.exception("An error occurred in password_reset_request: %s", str(e))

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    try:
        if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    messages.success(
                        request,
                        'Your password has been successfully reset. You can now log in with your new password.'
                    )
                    return redirect('password_reset_complete')
                else:
                    messages.error(
                        request,
                        'Passwords do not match. Please try again.'
                    )
                    return render(request, 'authentication/resetPassword/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
            return render(request, 'authentication/resetPassword/password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
        else:
            messages.error(
                request,
                'The password reset link is invalid or has expired. Please request a new one.'
            )
            return redirect('password_reset_request')
    except Exception as e:
        logger.exception("An error occurred in password_reset_confirm: %s", str(e))

def password_reset_done(request):
    try:
        return render(request, 'authentication/resetPassword/password_reset_done.html')
    except Exception as e:
        logger.exception("An error occurred in password_reset_done: %s", str(e))

def password_reset_complete(request):
    try:
        return render(request, 'authentication/resetPassword/password_reset_complete.html')
    except Exception as e:
        logger.exception("An error occurred in password_reset_complete: %s", str(e))
