from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
#from BookLab.decorators import check_recaptcha

from .forms import SignUpForm, loginform, UserForgotPasswordForm, UserPasswordResetForm
from .tokens import account_activation_token, password_reset_token

@login_required
def home_view(request):
    return render(request, 'home.html')

def activation_sent_view(request):
    return render(request, 'activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        us = Profile.objects.filter(user=user)
        if not us:
            us = Profile.objects.create(user=user)
        #user.profile.first_name = user.first_name
        #user.profile.last_name = user.last_name
        #user.profile.email = user.email
        #user.profile.signup_confirmation = True
        # set signup_confirmation true
        #user.profile.signup_confirmation = True
        us.first_name = user.first_name
        us.last_name = user.last_name
        us.email = user.email
        us.signup_confirmation = True
        us.save()
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()

            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template()
            # and calls its render() method immediately.
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'signup.html', {'form': form, 'msg':'U need to verify ur email'})
            else:
                return redirect('signup')
    form = loginform()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def password_reset(request):
    """User forgot password form view."""
    msg = ''
    if request.method == "POST":
        form = UserForgotPasswordForm(request.POST)
        if form.is_valid():
            email = request.POST.get('username')
            qs = User.objects.filter(username=email)
            site = get_current_site(request)

            if len(qs) > 0:
                user = qs[0]
                user.is_active = False  # User needs to be inactive for the reset password duration
                #user.profile.reset_password = True
                user.save()
                subject = 'Reset password for domain.com',
                message = render_to_string('password_reset_mail.html', {
                    'user': user,
                    'protocol': 'http',
                    'domain': site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                return redirect('activation_sent')
            else:
                return HttpResponse('No email found')

        #         message = Mail(
        #             from_email='noreply@domain.com',
        #             to_emails=email,
        #             subject='Reset password for domain.com',
        #             html_content=message)
        #         try:
        #             sg = SendGridAPIClient(config['SENDGRID_API_KEY'])
        #             response = sg.send(message)
        #         except Exception as e:
        #             print(e)
        #
        #     messages.add_message(request, messages.SUCCESS, 'Email {0} submitted.'.format(email))
        #     msg = 'If this mail address is known to us, an email will be sent to your account.'
        # else:
        #     messages.add_message(request, messages.WARNING, 'Email not submitted.')
        #     return render(request, 'account/password_reset_req.html', {'form': form})

    return render(request, 'password_reset_req.html', {'form': UserForgotPasswordForm, 'msg': msg})


def reset(request, uidb64, token):

    if request.method == 'POST':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            #messages.add_message(request, messages.WARNING, str(e))
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            form = UserPasswordResetForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)

                user.is_active = True
                #user.profile.reset_password = False
                user.save()
                #messages.add_message(request, messages.SUCCESS, 'Password reset successfully.')
                return redirect('login')
            else:
                context = {
                    'form': form,
                    'uid': uidb64,
                    'token': token
                }
                #messages.add_message(request, messages.WARNING, 'Password could not be reset.')
                return render(request, 'password_reset_conf.html', context)
        # else:
        #     messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
        #     messages.add_message(request, messages.WARNING, 'Please request a new password reset.')
        else:
            return render(request, 'activation_invalid.html')

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        #messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        context = {
            'form': UserPasswordResetForm(user),
            'uid': uidb64,
            'token': token
        }
        return render(request, 'password_reset_conf.html', context)
    # else:
    #     messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
    #     messages.add_message(request, messages.WARNING, 'Please request a new password reset.')
    else:
        return redirect('home')
        #return render(request, 'activation_invalid.html')





