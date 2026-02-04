from adrf.viewsets import ViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from asgiref.sync import sync_to_async
from api.serializers.businesses import BusinessListSerializer
from core.models import Business
from django.db.models import F, ExpressionWrapper, FloatField, Value
import math

class BusinessListView(ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    @sync_to_async
    def _get_businesses(self, iae_code, lat, lon, radius):
        lat_range = radius / 111000 
        lon_range = radius / (111000 * math.cos(math.radians(lat)))
        
        businesses = Business.objects.filter(
            coordinates__lat__gte=lat - lat_range,
            coordinates__lat__lte=lat + lat_range,
            coordinates__lon__gte=lon - lon_range,
            coordinates__lon__lte=lon + lon_range
        )
        
        if iae_code:
            businesses = businesses.filter(
                iae_code__contains=iae_code[0:2],
            )
            
        businesses = businesses.annotate(
            metrics_score=ExpressionWrapper(
                Value(0.2) * (F('rentability') / Value(100.0)) +
                Value(0.4) * F('tipology') +
                Value(0.4) * (Value(1.0) / (Value(1) + F('proximity_to_urban_center_m'))),
                output_field=FloatField()
            )
        ).order_by('-metrics_score')
        serializer = BusinessListSerializer(businesses, many=True)
        return serializer.data
        
    async def list(self, request):
        """List all businesses"""
        iae_code = request.GET.get('iae_code')
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        radius = request.GET.get('radius')
        if not lat or not lon or not radius:
            raise ValueError("Missing required parameters: lat, lon, radius")

        # Get from database        
        data = await self._get_businesses(iae_code, float(lat), float(lon), int(radius))
        
        return Response(data, status=status.HTTP_200_OK)
    