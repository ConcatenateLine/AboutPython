from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

class CustomLoginRequiredMixin():
    login_url = 'polls:login'
    exclude_url = ['/logout/']

    def __init__(self, get_response):
        self.get_response = get_response

    def handle_no_permission(self, request):
        response = HttpResponseRedirect(reverse(self.login_url) + '?next=' + request.path)
        response.delete_cookie('Authorization')

        messages.error(request, 'You are not logged in.')

        # Redirect to a custom page or perform any other action
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        if getattr(view_func, 'is_public', False) or request.path in self.exclude_url or request.path.startswith('/api/'):
            # If the request is public determinated by the decorator @public_path, allow it to proceed
            return None

        # if not public, check for authentication
        token = request.COOKIES.get('Authorization')

        if not token:
            return self.handle_no_permission(request)
        
        try:
            validated_token = RefreshToken(token, False)

            user_id = validated_token.get('user_id')
            request.user = User.objects.get(id=user_id)

        except Exception as e:
            return self.handle_no_permission(request)
        
        if not request.user.is_authenticated:
            return self.handle_no_permission(request)
            
        # If the user is authenticated, allow the request to proceed
        return None


    def __call__(self, request):
        return self.get_response(request)