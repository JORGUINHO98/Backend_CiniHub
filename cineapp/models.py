from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# =========================
# USUARIO PERSONALIZADO
# =========================
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un correo electrónico")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    avatar = models.URLField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    pais = models.CharField(max_length=100, blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.email


# =========================
# ROLES Y PERMISOS
# =========================
class Permiso(models.Model):
    descripcion = models.TextField(blank=True)
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    nombre = models.CharField(max_length=150)
    permisos = models.ManyToManyField(Permiso, related_name="roles", blank=True)

    def __str__(self):
        return self.nombre


# =========================
# FAVORITOS Y VISTOS
# =========================
class Favorito(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="favoritos",
        on_delete=models.CASCADE
    )
    id_pelicula = models.IntegerField()
    lista_de_pelicula = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Favorito {self.id_pelicula} de {self.usuario}"


class Visto(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="vistos",
        on_delete=models.CASCADE
    )
    id_pelicula = models.IntegerField()  # ID de TMDb
    titulo = models.CharField(max_length=255)
    calificacion = models.IntegerField(null=True, blank=True)
    fecha_visto = models.DateTimeField(auto_now_add=True)
    nota_personal = models.TextField(blank=True)
    porcentaje_visto = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.titulo} visto por {self.usuario}"


# =========================
# PELICULA
# =========================
class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    poster = models.URLField(null=True, blank=True)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)  # 🔑 Para no duplicar

    def __str__(self):
        return self.titulo


# =========================
# SUSCRIPCIÓN
# =========================
class PlanSuscripcion(models.Model):
    TIPO_CHOICES = [
        ('basico', 'Básico'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, unique=True)
    precio_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    caracteristicas = models.JSONField(default=list)  # Lista de características
    max_dispositivos = models.IntegerField(default=1)
    calidad_maxima = models.CharField(max_length=20, default='HD')  # HD, Full HD, 4K
    es_activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio_mensual}/mes"


class Suscripcion(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('suspendida', 'Suspendida'),
        ('cancelada', 'Cancelada'),
        ('expirada', 'Expirada'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="suscripciones",
        on_delete=models.CASCADE
    )
    plan = models.ForeignKey(PlanSuscripcion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField()
    fecha_renovacion = models.DateTimeField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=50, blank=True)
    es_renovacion_automatica = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.email} - {self.plan.nombre}"

    @property
    def esta_activa(self):
        from django.utils import timezone
        return (self.estado == 'activa' and self.fecha_fin > timezone.now())


class HistorialPago(models.Model):
    suscripcion = models.ForeignKey(
        Suscripcion,
        on_delete=models.CASCADE,
        related_name='pagos'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50)
    transaccion_id = models.CharField(max_length=100, unique=True)
    estado = models.CharField(max_length=20, default='completado')

    def __str__(self):
        return f"Pago {self.transaccion_id} - ${self.monto}"
