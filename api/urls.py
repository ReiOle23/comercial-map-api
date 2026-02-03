from django.urls import path
from api.views.users.user_list_create import UserListView, UserRegisterView
from api.views.users.user_detail import UserDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views.businesses.business_list import BusinessListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='users'),
    path('users/register/', UserRegisterView.as_view(), name='user_register'),
    path('user/login/', TokenObtainPairView.as_view(), name='user_login'),
    path('user/refresh/', TokenRefreshView.as_view(), name='user_refresh'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    
    # GET /businesses?lat=41.38879&lon=2.15899&radius=5000
    path('businesses/', BusinessListView.as_view(), name='businesses'),
    
    
#     1. Dado un punto de coordenadas: latitud y longitud y un radio máximo de ataque (en metros),
# devolver los negocios, ordenados de mayor a menor métrica de conversión, junto con sus
# coordenadas y otra información relevante.
]
