from rest_framework import serializers
from core.models import Business

class BusinessListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('id', 'name', 'iae_code', 'rentability', 'proximity_to_urban_center_m', 'coordinates')
        