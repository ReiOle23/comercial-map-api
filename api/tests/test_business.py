import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Business
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.mark.django_db(transaction=True)
class TestBusinessLoad:
    
    @pytest.fixture(autouse=True)
    def setup(self, db):
        """Setup test data"""
        # Create businesses
        for i in range(20):
            Business.objects.create(
                name=f'Business {i}',
                iae_code='56101',
                rentability=70 + i,
                proximity_to_urban_center_m=1000 + i * 100,
                coordinates={'lat': 41.38879 + i * 0.001, 'lon': 2.15899 + i * 0.001}
            )
        
        self.businesses_url = reverse('api:businesses')
        # Create user directly
        self.user = User.objects.create_user(
            username='loadtestuser',
            email='loadtest@example.com',
            password='loadtest_password',
            first_name='Load',
            last_name='Test'
        )
        
        # Generate token
        refresh = RefreshToken.for_user(self.user)
        self.auth_token = str(refresh.access_token)
        
    @pytest.mark.asyncio
    async def test_get_businesses(self):
        """Test getting businesses"""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.auth_token}')
        response = await sync_to_async(client.get)(self.businesses_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 20
        