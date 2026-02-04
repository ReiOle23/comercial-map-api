from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

def test_crud_iae_endpoints(db):
    """Test IAE CRUD endpoints"""
    client = APIClient()
    user = User.objects.create_user(
        username='loadtestuser',
        email='loadtest@example.com',
        password='loadtest_password',
        first_name='Load',
        last_name='Test'
    )
    
    # Generate token
    refresh = RefreshToken.for_user(user)
    auth_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
    # Create new iae
    data = {
        'code': '1234',
        'value': 1000
    }
    response = client.post(reverse('api:iaecodes'), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('code') == '1234'
    assert response.json().get('value') == 1000
    # List iae
    response = client.get(reverse('api:iaecodes'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    # Get iae
    response = client.get(reverse('api:iaecode_detail', args=[1]))
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('code') == '1234'
    assert response.json().get('value') == 1000
    # Update iae
    iae_id = response.json().get('id')  # Get the actual ID from creation response
    data = {
        'value': 200
    }
    response = client.patch(reverse('api:iaecode_detail', args=[iae_id]), data=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('code') == '1234'
    assert response.json().get('value') == 200
    # Delete iae
    response = client.delete(reverse('api:iaecode_detail', args=[iae_id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
