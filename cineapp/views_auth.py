# cineapp/views_auth.py
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from datetime import timedelta

from .models import Usuario, PlanSuscripcion, Suscripcion, HistorialPago
from .serializers import (
    UsuarioRegisterSerializer, UsuarioSerializer, UsuarioLoginSerializer,
    PlanSuscripcionSerializer, SuscripcionSerializer,
    CrearSuscripcionSerializer, HistorialPagoSerializer
)

# =========================
# Registro
# =========================
class RegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioRegisterSerializer
    permission_classes = (AllowAny,)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'nombre': user.nombre
                }
            }, status=status.HTTP_201_CREATED)
        return Response({'error': 'Datos inválidos', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# =========================
# Login personalizado
# =========================
class LoginView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = UsuarioLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = Usuario.objects.get(email=email)
                if user.check_password(password) and user.is_active:
                    jwt_serializer = EmailTokenObtainPairSerializer(data=request.data)
                    if jwt_serializer.is_valid():
                        return Response(jwt_serializer.validated_data, status=status.HTTP_200_OK)
                return Response({"error": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
            except Usuario.DoesNotExist:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# =========================
# Logout
# =========================
class LogoutView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        return Response({"message": "Sesión cerrada exitosamente"}, status=status.HTTP_200_OK)

# =========================
# JWT con email
# =========================
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

# =========================
# Perfil
# =========================
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

# =========================
# Suscripciones
# =========================
class PlanesSuscripcionView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        planes = PlanSuscripcion.objects.filter(es_activo=True)
        serializer = PlanSuscripcionSerializer(planes, many=True)
        return Response(serializer.data)


class SuscripcionUsuarioView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        suscripcion = Suscripcion.objects.filter(usuario=request.user, estado='activa').first()
        if suscripcion:
            serializer = SuscripcionSerializer(suscripcion)
            return Response(serializer.data)
        return Response({"message": "No tienes suscripción activa"}, status=404)
    
    def post(self, request):
        serializer = CrearSuscripcionSerializer(data=request.data)
        if serializer.is_valid():
            plan_id = serializer.validated_data['plan_id']
            metodo_pago = serializer.validated_data['metodo_pago']
            es_renovacion_automatica = serializer.validated_data['es_renovacion_automatica']
            try:
                plan = PlanSuscripcion.objects.get(id=plan_id, es_activo=True)
            except PlanSuscripcion.DoesNotExist:
                return Response({"error": "Plan no encontrado"}, status=404)
            
            Suscripcion.objects.filter(usuario=request.user, estado='activa').update(estado='cancelada')
            fecha_fin = timezone.now() + timedelta(days=30)
            suscripcion = Suscripcion.objects.create(
                usuario=request.user,
                plan=plan,
                fecha_fin=fecha_fin,
                metodo_pago=metodo_pago,
                es_renovacion_automatica=es_renovacion_automatica
            )
            HistorialPago.objects.create(
                suscripcion=suscripcion,
                monto=plan.precio_mensual,
                metodo_pago=metodo_pago,
                transaccion_id=f"TXN_{suscripcion.id}_{timezone.now().timestamp()}"
            )
            return Response(SuscripcionSerializer(suscripcion).data, status=201)
        return Response(serializer.errors, status=400)


class CancelarSuscripcionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        suscripcion = Suscripcion.objects.filter(usuario=request.user, estado='activa').first()
        if not suscripcion:
            return Response({"error": "No tienes suscripción activa"}, status=404)
        suscripcion.estado = 'cancelada'
        suscripcion.save()
        return Response({"message": "Suscripción cancelada exitosamente"})


class HistorialPagosView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        suscripciones = Suscripcion.objects.filter(usuario=request.user)
        pagos = HistorialPago.objects.filter(suscripcion__in=suscripciones).order_by('-fecha_pago')
        serializer = HistorialPagoSerializer(pagos, many=True)
        return Response(serializer.data)
