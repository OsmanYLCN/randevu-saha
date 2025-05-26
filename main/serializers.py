from rest_framework import serializers
from .models import Halisaha

class HaliSahaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Halisaha
        fields = '__all__'