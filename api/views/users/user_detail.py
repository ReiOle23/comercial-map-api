from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from api.serializers.users import UserListSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]