from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework_simplejwt.tokens import RefreshToken


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'polls:login'
    redirect_field_name = 'redirect_to'
    exclude_url = ['/logout/']

    def handle_no_permission(self, request):
        response = HttpResponseRedirect(reverse(self.login_url) + '?next=' + request.path)
        response.delete_cookie('Authorization')

        messages.error(request, 'You are not logged in.')

        # Redirect to a custom page or perform any other action
        return response

    def dispatch(self, request, *args, **kwargs):

        if request.path in self.exclude_url or request.path.startswith('/api/'):
            # If the request is excluded, allow it to proceed
            return super().dispatch(request, *args, **kwargs)

        # if not excluded, check for authentication
        token = request.COOKIES.get('Authorization')

        if not token:
            return self.handle_no_permission(request)
        
        try:
            validated_token = RefreshToken(token, True)

            user_id = validated_token.get('user_id')
            request.user = User.objects.get(id=user_id)

        except Exception as e:
            return self.handle_no_permission(request)
        
        if not request.user.is_authenticated:
            return self.handle_no_permission(request)
            
        # If the user is authenticated, allow the request to proceed
        return super().dispatch(request, *args, **kwargs)
