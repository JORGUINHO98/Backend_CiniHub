# cineapp/views_jwt.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers_jwt import EmailTokenObtainPairSerializer
from .serializers import UsuarioSerializer
from .models import Visto, Favorito

# ✅ Login con email
class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

# ✅ Perfil con métricas incluidas (respuesta aplanada)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)

        # Métricas adicionales
        vistos = Visto.objects.filter(usuario=request.user)
        favoritos = Favorito.objects.filter(usuario=request.user)

        promedio = (
            round(sum(v.calificacion or 0 for v in vistos) / len(vistos), 1)
            if len(vistos) > 0 else 0
        )

        # 👇 Devolvemos todo plano, fácil de consumir en frontend
        return Response({
            **serializer.data,  # Se expande el dict con los datos del usuario
            "stats": {
                "vistos": len(vistos),
                "favoritos": len(favoritos),
                "promedioCalificacion": promedio
            }
        })
