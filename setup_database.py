#!/usr/bin/env python3
"""
Script para configurar la base de datos con datos iniciales
Ejecutar con: python manage.py shell < setup_database.py
"""

from django.contrib.auth import get_user_model
from cineapp.models import PlanSuscripcion, Suscripcion
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

print("🚀 Configurando base de datos de CineHub...")

# 1. Crear planes de suscripción
print("\n📋 Creando planes de suscripción...")

plans_data = [
    {
        'nombre': 'Básico',
        'tipo': 'basico',
        'precio_mensual': 9.99,
        'descripcion': 'Perfecto para comenzar tu experiencia cinematográfica',
        'caracteristicas': [
            'Acceso a películas en HD',
            '1 dispositivo simultáneo',
            'Catálogo básico de películas',
            'Sin anuncios',
            'Soporte por email'
        ],
        'max_dispositivos': 1,
        'calidad_maxima': 'HD',
        'es_activo': True
    },
    {
        'nombre': 'Premium',
        'tipo': 'premium',
        'precio_mensual': 15.99,
        'descripcion': 'La experiencia completa de entretenimiento',
        'caracteristicas': [
            'Acceso a películas en Full HD',
            '3 dispositivos simultáneos',
            'Catálogo completo de películas',
            'Sin anuncios',
            'Descarga para offline',
            'Soporte prioritario',
            'Acceso anticipado a estrenos'
        ],
        'max_dispositivos': 3,
        'calidad_maxima': 'Full HD',
        'es_activo': True
    },
    {
        'nombre': 'VIP',
        'tipo': 'vip',
        'precio_mensual': 24.99,
        'descripcion': 'La experiencia premium definitiva',
        'caracteristicas': [
            'Acceso a películas en 4K Ultra HD',
            'Dispositivos ilimitados',
            'Catálogo completo + contenido exclusivo',
            'Sin anuncios',
            'Descarga ilimitada para offline',
            'Soporte VIP 24/7',
            'Acceso anticipado a estrenos',
            'Contenido original exclusivo',
            'Eventos especiales'
        ],
        'max_dispositivos': 10,
        'calidad_maxima': '4K',
        'es_activo': True
    }
]

# Eliminar planes existentes
PlanSuscripcion.objects.all().delete()
print("✅ Planes existentes eliminados.")

# Crear nuevos planes
for plan_data in plans_data:
    plan = PlanSuscripcion.objects.create(**plan_data)
    print(f"✅ Plan creado: {plan.nombre} - ${plan.precio_mensual}/mes")

# 2. Crear usuario de prueba
print("\n👤 Creando usuario de prueba...")

# Eliminar usuario de prueba existente si existe
User.objects.filter(email="test@cinehub.com").delete()

# Crear usuario de prueba
test_user = User.objects.create_user(
    email="test@cinehub.com",
    nombre="Usuario de Prueba",
    password="test123"
)
print(f"✅ Usuario de prueba creado: {test_user.email}")

# 3. Crear suscripción de prueba
print("\n💳 Creando suscripción de prueba...")

# Obtener plan premium
premium_plan = PlanSuscripcion.objects.get(tipo='premium')

# Crear suscripción
fecha_fin = timezone.now() + timedelta(days=30)
test_subscription = Suscripcion.objects.create(
    usuario=test_user,
    plan=premium_plan,
    fecha_fin=fecha_fin,
    metodo_pago="tarjeta",
    es_renovacion_automatica=True
)
print(f"✅ Suscripción creada: {test_user.email} - {premium_plan.nombre}")

print(f"\n🎉 ¡Configuración completada!")
print(f"\n📊 Resumen:")
print(f"- Usuarios: {User.objects.count()}")
print(f"- Planes: {PlanSuscripcion.objects.count()}")
print(f"- Suscripciones: {Suscripcion.objects.count()}")

print(f"\n🔑 Credenciales de prueba:")
print(f"Email: test@cinehub.com")
print(f"Password: test123")
print(f"Plan: Premium")

print(f"\n🌐 URLs del API:")
print(f"- Login: http://localhost:5051/api/auth/login/")
print(f"- Register: http://localhost:5051/api/auth/register/")
print(f"- Profile: http://localhost:5051/api/auth/profile/")
print(f"- Plans: http://localhost:5051/api/subscription/plans/")
