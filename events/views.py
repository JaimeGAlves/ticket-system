from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import random

from events.models import Patrocinador

from events.serializers import PatrocinadorSerializer

class TesteView(APIView):
    
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello, world!"})
    

class PatrocinadorCreateView(APIView):
    
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PatrocinadorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PatrocinadorDetalhesView(APIView):
    
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """Retorna o último registro do patrocinador
           Chave primária: pk
        """
        result = Patrocinador.objects.filter(pk=pk).last()
        
        return result
    
    def get(self, request, pk=None):
        
        if pk:
            patrocinador = self.get_object(pk)
            if patrocinador:
                serializer = PatrocinadorSerializer(patrocinador)
                return Response(serializer.data)
            return Response({"message": "Patrocinador não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        patrocinadores = Patrocinador.objects.all()
        
        serializer = PatrocinadorSerializer(patrocinadores, many=True)
        
        return Response(serializer.data)
    
    def put(self, request, pk):
        
        patrocinador = self.get_object(pk)
        serializer = PatrocinadorSerializer(patrocinador, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        
        patrocinador = self.get_object(pk)
        patrocinador.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class PatrocinadoresAppView(APIView):
    
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        patrocinadores = list(Patrocinador.objects.order_by('id'))
        patrocinadores_randomizados = random.sample(patrocinadores, len(patrocinadores))
        imagens_urls = [
            request.build_absolute_uri(patrocinador.imagem_app.url)
            for patrocinador in patrocinadores_randomizados
        ]

        return Response(imagens_urls)
    

class PatrocinadoresSiteView(APIView):
    
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        patrocinadores = list(Patrocinador.objects.order_by('id'))
        patrocinadores_randomizados = random.sample(patrocinadores, len(patrocinadores))
        imagens_urls = [
            request.build_absolute_uri(patrocinador.imagem_site.url)
            for patrocinador in patrocinadores_randomizados
        ]

        return Response(imagens_urls)

# from django.shortcuts import render, redirect, get_object_or_404
# from django.views import View
# from django.contrib.auth.decorators import login_required
# from events.models import Patrocinador
# from .forms import SponsorForm
# from .utils import reorganize_sponsor_ids
# from django.contrib import messages
# import logging

# logger = logging.getLogger(__name__)

# class eventsCreateView(View):
#     def get(self, request):
#         events = Sponsor.objects.all()
#         return render(request, 'events/events.html', {'events': events})

#     def post(self, request):
#         form = SponsorForm(request.POST, request.FILES)
#         if form.is_valid():
#             new_sponsor = form.save(commit=False)
#             next_id = reorganize_sponsor_ids()
#             new_sponsor.id = next_id
#             new_sponsor.save()
#             messages.success(request, "O patrocinador " + form.cleaned_data['name'] + " foi adicionado com sucesso.")
#             return redirect('sponsor_list')
#         else:
#             messages.error(request, "Erro ao adicionar o patrocinador. Por favor, verifique os dados e tente novamente.")
#         events = Sponsor.objects.all()
#         return render(request, 'events/events.html', {'form': form, 'events': events})
                  
# def delete_sponsor(request, id):
#     sponsor = get_object_or_404(Sponsor, id=id)
#     sponsor.delete()
#     reorganize_sponsor_ids()
#     return redirect('sponsor_list')

# class NoticesDashboardView(View):
#     def get(self, request):
#         return render(request, 'notices/dashboard.html')