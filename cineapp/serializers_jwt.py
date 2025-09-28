# cineapp/serializers_jwt.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para que JWT use el email
    como identificador en lugar de username.
    """
    username_field = "email"

    def validate(self, attrs):
        """
        Extiende la validación para devolver también datos básicos del usuario
        junto con el token JWT.
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Tokens
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        # Datos extra del usuario
        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "nombre": getattr(self.user, "nombre", ""),
            "is_active": self.user.is_active,
        }

        return data
