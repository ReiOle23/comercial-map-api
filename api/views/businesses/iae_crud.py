from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers.iae import IaeSerializer
from core.models import IaeCode

class IaeView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = IaeCode.objects.all()
    serializer_class = IaeSerializer
    
class IaeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = IaeCode.objects.all()
    serializer_class = IaeSerializer