from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .models import CustomUser
from .serializers import LoginSerializer, RegisterSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            current_site = get_current_site(request)
            verification_url = reverse('verify_email', kwargs={'token': user.email_verification_token})
            full_verification_url = f"http://{current_site.domain}{verification_url}"

            html_content = render_to_string('email_verification_template.html', {'user': user, 'verification_url': full_verification_url})
            text_content = strip_tags(html_content)


            msg = EmailMultiAlternatives(
                subject=' Verify your email address',
                body = text_content,
                from_email ='info@videoflix.steffen-winter.org',
                to = [user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return Response({'message': 'Check your Email for verification link'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            user = CustomUser.objects.get(email_verification_token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid verification token.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.email_verification_token = None
        user.save()

        frontend_login_url = 'http://localhost:4200/log-in'
        return redirect(frontend_login_url)
    

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        print('Received login request. Data:', request.data)
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request=request, username=email, password=password)

            if user:
                if not user.is_verified:
                    return Response({'error': 'Email is not verified yet.'}, status=status.HTTP_403_FORBIDDEN)

                token, created = Token.objects.get_or_create(user=user)

                response_data = {
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
                return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No token found for user, user not logged in'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_url = f"http://localhost:4200/reset-password/{user.pk}/{token}/"

            html_content = render_to_string('email_password_reset.html', {'verification_url': reset_url})
            text_content = f"Please reset your password using the following link: {reset_url}"

            msg = EmailMultiAlternatives(
                subject="Reset your password",
                body=text_content,
                from_email='kontakt@steffen-winter.org',
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return Response({"message": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, user_id, token):
        user = CustomUser.objects.filter(pk=user_id).first()

        if not user or not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


