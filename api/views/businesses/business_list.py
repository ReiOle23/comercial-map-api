from adrf import generics
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.serializers.businesses import BusinessListSerializer
from core.models import Business

class BusinessListView(generics.ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessListSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    