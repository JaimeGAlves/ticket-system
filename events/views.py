from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import random

# from events.models import Patrocinador

# from events.serializers import PatrocinadorSerializer

class TesteView(APIView):
    
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, world!"})
    