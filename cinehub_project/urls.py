from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# 👋 Vista para la ruta raíz
def root_view(request):
    return JsonResponse({"message": "Welcome to CineHub API 🎬"})

urlpatterns = [
    path("", root_view, name="root"),          # Ruta raíz
    path("admin/", admin.site.urls),           # Admin de Django
    path("api/", include("cineapp.urls")),     # Todas las rutas de cineapp bajo /api/
]
