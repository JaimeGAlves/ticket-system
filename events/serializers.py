from rest_framework import serializers
from events.models import Patrocinador

class PatrocinadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patrocinador
        fields = '__all__'
