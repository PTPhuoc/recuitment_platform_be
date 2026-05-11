from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, ExpiredTokenError
from app.models import Account
from app.serializers.account_serializer import AccountSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import get_object_or_404
import random


def send_email(subject, email, data, template_name):
    html_message = render_to_string(template_name, data)
    send_mail(
        subject=subject,
        message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message
    )


class AuthAPI(viewsets.ModelViewSet):
    @action(methods=['post'], detail=False)
    def login(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember', False)
        if not email or not password:
            return Response({'status': 'Empty data', 'message': 'Email or Password is required'},
                            status=status.HTTP_200_OK)

        user = get_object_or_404(Account, email=email)
        if not check_password(password, user.password):
            return Response({'status': 'Not match', 'message': 'Password is incorrect'},
                            status=status.HTTP_200_OK)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response = Response({'status': 'Success', 'user': AccountSerializer(user).data},
                            status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=3600,
            path='/'
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=1209600 if remember else 86400,
            path='/'
        )
        return response

    @action(methods=['get'], detail=False)
    def logout(self):
        response = Response({'status': 'Success'}, status=status.HTTP_200_OK)
        response.delete_cookie(key='access_token')
        response.delete_cookie(key='refresh_token')
        return response

    @action(methods=['post'], detail=False)
    def signup(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        phone_number = data.get('phoneNumber', '')
        if not email or not password:
            return Response({'status': 'Empty data', 'message': 'Email or password is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = Account.objects.filter(email=email).first()
        if user:
            return Response({'status': 'Data exist', 'message': 'Email already exist'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Account.objects.create_user(email=email, password=password, phoneNumber=phone_number, role='pending')
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response = Response({'status': 'Success', 'user': AccountSerializer(user).data},
                                status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=3600, path='/'
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh), httponly=True,
                secure=False, samesite='Lax',
                max_age=604800, path='/'
            )
            return response
        except Exception as e:
            return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def send_code(self, request):
        data = request.data
        email = data.get('email')
        if not email:
            return Response({'status': 'Empty data', 'message': 'Email is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            code = f"{random.randint(10000, 99999):06d}"
            cache.set(f"otp:{email}", code, timeout=360)
            send_email("Mã xác nhận đăng ký FUJobs", email,
                       {'username': email, 'code': code, 'site_url': settings.SITE_URL}, "confirm_email.html")
            return Response({'status': 'Success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def verify_code(self, request):
        data = request.data
        email = data.get('email')
        client_otp = data.get('otp')
        if not email:
            return Response({'status': 'Empty data', 'message': 'Email is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        otp = cache.get(f"otp:{email}")
        if not otp:
            return Response({'status': 'Empty data', 'message': 'OTP not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if otp != client_otp:
            return Response({'status': 'Not match', 'message': 'OTP do not match'}, status=status.HTTP_400_BAD_REQUEST)

        cache.delete(f"otp:{email}")
        return Response({'status': 'Success'}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def refresh_token(self, request):
        token = request.COOKIES.get('refresh_token')
        if not token:
            return Response({'status': 'Empty data', 'message': 'Token is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(token)
            new_access = str(refresh.access_token)
            response = Response({'status': 'Success', 'message': 'Token refreshed'}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=new_access,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=3600,
                path='/'
            )
            return response
        except InvalidToken:
            return Response({'status': 'Invalid token', 'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except ExpiredTokenError:
            return Response({'status': 'Token Expired', 'message': 'Need login again'},
                            status=status.HTTP_400_BAD_REQUEST)
