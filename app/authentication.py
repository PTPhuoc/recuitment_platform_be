from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, ExpiredTokenError
from rest_framework.exceptions import AuthenticationFailed

from app.models import Account


class CookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return super().authenticate(request)

        try:
            validated_token = self.get_validated_token(access_token)
            user_id = validated_token.get('user_id')
            if not user_id:
                raise InvalidToken('Missing user_id')
            user = Account.objects.get(id=user_id)
            return user, validated_token
        except ExpiredTokenError as e:
            raise AuthenticationFailed({
                'status': 'Token expired',
                'code': 'token_expired',
                'message': str(e)
            })
        except InvalidToken as e:
            raise AuthenticationFailed({
                'status': 'Invalid token',
                'code': 'token_invalid',
                'message': str(e)
            })
