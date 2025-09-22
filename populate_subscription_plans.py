#!/usr/bin/env python3
"""
Script para poblar la base de datos con planes de suscripción
Ejecutar con: python manage.py shell < populate_subscription_plans.py
"""

from cineapp.models import PlanSuscripcion

# Crear planes de suscripción
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
print("Planes existentes eliminados.")

# Crear nuevos planes
for plan_data in plans_data:
    plan = PlanSuscripcion.objects.create(**plan_data)
    print(f"Plan creado: {plan.nombre} - ${plan.precio_mensual}/mes")

print(f"\n✅ Se crearon {len(plans_data)} planes de suscripción exitosamente!")
print("\nPlanes disponibles:")
for plan in PlanSuscripcion.objects.all():
    print(f"- {plan.nombre}: ${plan.precio_mensual}/mes ({plan.tipo})")
