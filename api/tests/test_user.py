from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class UserAPITestCase(TestCase):
    
    # for each test
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'test_password',
            'password2': 'test_password',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.login_url = reverse('api:user_login')

    def create_user_via_api(self, user_data=None):
        """Helper method to create a user via the API"""
        register_url = reverse('api:user_register')
        data = user_data or self.user_data
        return self.client.post(register_url, data=data)

    def test_user_register(self):
        """Test user registration endpoint"""
        response = self.create_user_via_api()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)
    
    def test_user_login(self):
        """Test user login endpoint"""
        # Create user first
        self.create_user_via_api()
        
        # Now login
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, data=login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials"""
        login_data = {
            'username': 'nonexistent',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data=login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_unauthenticated(self):
        url = reverse('api:users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail(self):
        """Test user detail endpoint"""
        # Create user and get tokens
        response = self.create_user_via_api()
        data = response.json()
        access_token = data['access']
        
        # Get user from database
        user = User.objects.get(username=self.user_data['username'])
        
        # Set authentication header with Bearer token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Get user details (now authenticated)
        url = reverse('api:user_detail', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['username'], self.user_data['username'])
        self.assertEqual(data['email'], self.user_data['email'])

    def test_token_refresh(self):
        """Test token refresh endpoint"""
        # Register and get tokens
        response = self.create_user_via_api()
        data = response.json()
        refresh_token = data['refresh']
        
        # Refresh token
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(reverse('api:user_refresh'), data=refresh_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)
