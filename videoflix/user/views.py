from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .models import CustomUser
from .serializers import RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Verifizierungslink erstellen
            current_site = get_current_site(request)
            verification_url = reverse('verify_email', kwargs={'token': user.email_verification_token})
            full_verification_url = f"http://{current_site.domain}{verification_url}"

            # E-Mail an den Benutzer senden
            send_mail(
                'Verify your email address',
                f'Hello {user.email},\n\nPlease Verify your mail here:\n{full_verification_url}',
                'kontakt@steffen-winter.org',  # Absender
                [user.email],  # Empfänger
                fail_silently=False,
            )

            return Response({'message': 'Check your Email for verification link'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            user = CustomUser.objects.get(email_verification_token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid verification token.'}, status=status.HTTP_400_BAD_REQUEST)

        # Benutzer verifizieren
        user.is_verified = True
        user.email_verification_token = None  # Optional: Token nach Nutzung löschen
        user.save()

        return Response({'message': 'Email successfully verified. You can now log in.'}, status=status.HTTP_200_OK)

