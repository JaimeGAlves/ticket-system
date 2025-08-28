from django.urls import path
from .views import MeView, HelloView

urlpatterns = [
    path("me/", MeView.as_view()),
    path("hello/", HelloView.as_view()),
]
