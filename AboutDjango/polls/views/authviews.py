
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, logout as django_logout, login as django_login

from django.urls import reverse
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from users.authentication.JWTAuthentication import JWTAuthentication

def login(request):
    form = AuthenticationForm()
    errors = []
    
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            django_login(request, user)
            jwtRefreshToken = RefreshToken.for_user(user)

            response = HttpResponseRedirect(reverse('polls:dashboard'))
            response.set_cookie(key='Authorization', value=str(jwtRefreshToken), httponly=True, secure=True)
            
            return response
        else:
            errors.append('Invalid username or password')

    return render(request, "auth/login.html", {"form": form, "errors": errors})

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
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


def register(request):
    form = UserCreationForm()
    errors = []

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # Add a success message
            messages.success(request, 'You have been registered successfully.')

            response = HttpResponseRedirect(reverse('polls:login'))
            response.delete_cookie('Authorization')

            return response
        else:
            errors.append(form.errors)
    
    return render(request, "auth/register.html", {"form": form , "errors": errors})
