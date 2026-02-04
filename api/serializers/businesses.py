from adrf.serializers import ModelSerializer
from core.models import Business

class BusinessListSerializer(ModelSerializer):
    class Meta:
        model = Business
        fields = ('id', 'name', 'iae_code', 'rentability', 'proximity_to_urban_center_m', 'coordinates')
        