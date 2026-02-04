from adrf.serializers import ModelSerializer
from rest_framework import serializers
from core.models import Business

class BusinessListSerializer(ModelSerializer):
    metrics_score = serializers.FloatField(read_only=True)
    class Meta:
        model = Business
        fields = ('id', 'name', 'iae_code', 
                  'tipology', 'rentability', 
                  'proximity_to_urban_center_m', 'coordinates',
                  'metrics_score')
        