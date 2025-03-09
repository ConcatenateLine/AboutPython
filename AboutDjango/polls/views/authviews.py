from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.urls import reverse

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from users.decorators import public_path

@public_path
def login(request):
    form = AuthenticationForm()
    errors = []
    next_url = request.GET.get('next', '')

    
    if request.method == 'POST':
        next_url = request.POST.get('next', '')
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if not next_url:
            next_url = reverse('polls:dashboard')

        if user is not None:
            django_login(request, user)
            jwtRefreshToken = RefreshToken.for_user(user)

            response = HttpResponseRedirect(next_url)
            response.set_cookie(key='Authorization', value=str(jwtRefreshToken), httponly=True, secure=True)
            
            return response
        else:
            errors.append('Invalid username or password')

    return render(request, "auth/login.html", {"form": form, "errors": errors, "next": next_url})


def logout(request):
    django_logout(request)
    token = request.COOKIES.get('Authorization')

    if token:
        # Blacklist the token
        try:
            outstanding_token = RefreshToken(token)
            outstanding_token.blacklist()
        except OutstandingToken.DoesNotExist:
            pass  # Token was not found in the outstanding tokens

    response = HttpResponseRedirect(reverse('polls:home'))
    response.delete_cookie('Authorization')

    return response

@public_path
def register(request):
    form = UserCreationForm()
    errors = []

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'You have been registered successfully.')

            response = HttpResponseRedirect(reverse('polls:login'))
            response.delete_cookie('Authorization')

            return response
        else:
            errors.append(form.errors)
    
    return render(request, "auth/register.html", {"form": form , "errors": errors})
