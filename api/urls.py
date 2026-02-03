from django.urls import path
from api.views.users.user_list_create import UserListView, UserRegisterView
from api.views.users.user_detail import UserDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='users'),
    path('users/register/', UserRegisterView.as_view(), name='user_register'),
    path('user/login/', TokenObtainPairView.as_view(), name='user_login'),
    path('user/refresh/', TokenRefreshView.as_view(), name='user_refresh'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    
]
