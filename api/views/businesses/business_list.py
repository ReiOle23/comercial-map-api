from rest_framework import generics, permissions
from core.models import Business
from api.serializers.businesses import BusinessListSerializer

class BusinessListView(generics.ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessListSerializer
    permission_classes = [permissions.IsAuthenticated]
  