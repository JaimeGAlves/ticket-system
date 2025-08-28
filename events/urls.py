from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from events.views import (
    TesteView, 
    # PatrocinadorCreateView,
    # PatrocinadorDetalhesView,
    # PatrocinadoresAppView,
    # PatrocinadoresSiteView,
)

urlpatterns = [
    # path('teste/', TesteView.as_view()),
    # path('patrocinador/cadastrar/', PatrocinadorCreateView.as_view()),
    # path('patrocinador/', PatrocinadorDetalhesView.as_view()),
    # path('patrocinador/<int:pk>/', PatrocinadorDetalhesView.as_view()),
    # path('patrocinador/editar/<int:pk>/', PatrocinadorDetalhesView.as_view()),
    # path('patrocinador/app/', PatrocinadoresAppView.as_view()),
    # path('patrocinador/site/', PatrocinadoresSiteView.as_view()),
]