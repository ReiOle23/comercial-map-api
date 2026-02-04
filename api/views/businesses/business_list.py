from adrf.viewsets import ViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from asgiref.sync import sync_to_async
from api.serializers.businesses import BusinessListSerializer
from core.models import Business

class BusinessListView(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    @sync_to_async
    def _get_businesses(self):
        businesses = Business.objects.all()
        serializer = BusinessListSerializer(businesses, many=True)
        return serializer.data
        
    async def list(self, request):
        """List all businesses"""
        # Get from database
       
        data = await self._get_businesses()
        
        return Response(data, status=status.HTTP_200_OK)
    