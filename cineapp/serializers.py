# cineapp/serializers.py
from rest_framework import serializers
from .models import Usuario, Rol, Permiso, Favorito, Visto, PlanSuscripcion, Suscripcion, HistorialPago, Pelicula

class UsuarioSerializer(serializers.ModelSerializer):
    suscripcion_activa = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = [
            "id", "email", "nombre", "is_active", "is_staff", "fecha_registro",
            "avatar", "telefono", "fecha_nacimiento", "pais", "suscripcion_activa"
        ]

    def get_suscripcion_activa(self, obj):
        suscripcion = obj.suscripciones.filter(estado='activa').first()
        if suscripcion and suscripcion.esta_activa:
            return SuscripcionSerializer(suscripcion).data
        return None


class UsuarioLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UsuarioRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, error_messages={
        'min_length': 'La contraseña debe tener al menos 6 caracteres.',
        'blank': 'La contraseña no puede estar vacía.'
    })
    email = serializers.EmailField(error_messages={
        'invalid': 'Ingresa un email válido.',
        'blank': 'El email no puede estar vacío.'
    })
    nombre = serializers.CharField(max_length=150, error_messages={
        'max_length': 'El nombre no puede tener más de 150 caracteres.',
        'blank': 'El nombre no puede estar vacío.'
    })
    telefono = serializers.CharField(required=False, allow_blank=True, max_length=20, error_messages={
        'max_length': 'El teléfono no puede tener más de 20 caracteres.'
    })
    pais = serializers.CharField(required=False, allow_blank=True, max_length=100, error_messages={
        'max_length': 'El país no puede tener más de 100 caracteres.'
    })

    class Meta:
        model = Usuario
        fields = ["id", "email", "nombre", "password", "telefono", "pais"]

    def validate_email(self, value):
        if Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este email.")
        return value

    def validate_nombre(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre es obligatorio.")
        return value.strip()

    def create(self, validated_data):
        try:
            user = Usuario(
                email=validated_data["email"],
                nombre=validated_data["nombre"],
                telefono=validated_data.get("telefono", ""),
                pais=validated_data.get("pais", "")
            )
            user.set_password(validated_data["password"])
            user.save()
            return user
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            raise serializers.ValidationError(f"Error al crear el usuario: {str(e)}")


class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = "__all__"


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"


class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = "__all__"


class VistoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visto
        fields = "__all__"


class PeliculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelicula
        fields = "__all__"


class PlanSuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanSuscripcion
        fields = "__all__"


class SuscripcionSerializer(serializers.ModelSerializer):
    plan = PlanSuscripcionSerializer(read_only=True)
    plan_id = serializers.IntegerField(write_only=True)
    esta_activa = serializers.ReadOnlyField()

    class Meta:
        model = Suscripcion
        fields = [
            "id", "plan", "plan_id", "estado", "fecha_inicio", "fecha_fin",
            "fecha_renovacion", "metodo_pago", "es_renovacion_automatica", "esta_activa"
        ]


class HistorialPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialPago
        fields = "__all__"


class CrearSuscripcionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    metodo_pago = serializers.CharField(max_length=50)
    es_renovacion_automatica = serializers.BooleanField(default=True)
