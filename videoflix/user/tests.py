from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import CustomUser
from django.contrib.auth.tokens import default_token_generator

class UserRegistrationTestCase(APITestCase):

    def test_registration(self):
        url = reverse('register')
        data = {
            'email': 'testuser@example.com',
            'password': 'strongpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='testuser@example.com').exists())

class UserLoginTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testlogin@example.com',
            password='password123'
        )

    def test_login(self):
        url = reverse('login')
        data = {
            'email': 'testlogin@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class UserLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='testlogout@example.com',
            password='password123'
        )
        self.client.login(email='testlogout@example.com', password='password123')
    
    def test_logout(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PasswordResetRequestTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='passwordreset@example.com',
            password='password123'
        )

    def test_password_reset_request(self):
        url = reverse('password_reset')
        data = {'email': 'passwordreset@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PasswordResetConfirmTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='passwordconfirm@example.com',
            password='password123'
        )

    def test_password_reset_confirm(self):
        token = default_token_generator.make_token(self.user)
        url = reverse('password_reset_confirm', kwargs={'user_id': self.user.pk, 'token': token})
        data = {'new_password': 'newpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)