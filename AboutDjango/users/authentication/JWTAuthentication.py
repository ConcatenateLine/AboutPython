from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('Authorization')

        if not token:
            return None  # No token provided

        try:
            validated_token = RefreshToken(token, True)
            
        except Exception as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')

        user_id  = validated_token.get('user_id')

        # Retrieve the user from the database
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)  # Return the user and None for the auth token
