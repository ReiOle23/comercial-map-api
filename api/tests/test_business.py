import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from core.models import Business
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import time,asyncio

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
        params = {
            'lat': 41.38879,
            'lon': 2.15899,
            'radius': 5000
        }
        response = await sync_to_async(client.get)(self.businesses_url, data=params)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 20
        
    @pytest.mark.asyncio
    async def test_get_businesses_with_ordered_metrics(self):
        """Test getting businesses with ordered metrics"""
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.auth_token}')
        params = {
            'lat': 41.38879,
            'lon': 2.15899,
            'radius': 5000
        }
        response = await sync_to_async(client.get)(self.businesses_url, data=params)
        first_metrics = response.json()[0]['metrics_score']
        for business in response.json():
            assert 'metrics_score' in business
            assert business['metrics_score'] <= first_metrics
            
        
    @pytest.mark.skip(reason="Skipping due to database connection issues")
    @pytest.mark.asyncio
    async def test_get_businesses_1000_request_at_once(self):
        """Test 1000 concurrent requests should complete in under 1 second"""
        start_time = time.time()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.auth_token}')
        params = {
            'lat': 41.38879,
            'lon': 2.15899,
            'radius': 5000
        }
        
        async def make_request():
            response = await sync_to_async(client.get)(self.businesses_url, data=params)
            assert response.status_code == status.HTTP_200_OK
            return response
        
        # Run 1000 requests concurrently
        tasks = [make_request() for _ in range(1000)]
        await asyncio.gather(*tasks)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Assert all requests completed in under 1 second
        assert total_time < 1.0, f"Too slow: {total_time:.3f}s"
        