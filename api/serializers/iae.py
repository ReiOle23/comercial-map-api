from rest_framework import serializers
from core.models import IaeCode

class IaeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IaeCode
        fields = ('id', 'code', 'value')
        