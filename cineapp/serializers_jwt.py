from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer para que JWT use el email como campo de login
    en lugar de username.
    """
    username_field = "email"
