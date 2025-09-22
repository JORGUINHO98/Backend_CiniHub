#!/usr/bin/env python3
"""
Script para configurar la base de datos SIN usuarios de prueba
Solo crea los planes de suscripción
"""

import os
import sys
import django
from datetime import timedelta
from django.utils import timezone

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinehub_project.settings')
django.setup()

from cineapp.models import PlanSuscripcion, Usuario

def setup_database():
    print("🗄️ Configurando base de datos...")
    
    # 1. Crear planes de suscripción
    print("\n📋 Creando planes de suscripción...")
    
    # Eliminar planes existentes
    PlanSuscripcion.objects.all().delete()
    
    plans_data = [
        {
            'nombre': 'Básico',
            'tipo': 'basico',
            'precio_mensual': 9.99,
            'descripcion': 'Acceso básico a contenido',
            'caracteristicas': [
                'Acceso a películas y series',
                'Calidad HD',
                '1 dispositivo simultáneo',
                'Sin anuncios'
            ],
            'max_dispositivos': 1,
            'calidad_maxima': 'HD',
            'es_activo': True
        },
        {
            'nombre': 'Premium',
            'tipo': 'premium',
            'precio_mensual': 14.99,
            'descripcion': 'Acceso premium con más beneficios',
            'caracteristicas': [
                'Acceso a todo el contenido',
                'Calidad Full HD',
                '2 dispositivos simultáneos',
                'Sin anuncios',
                'Descarga offline'
            ],
            'max_dispositivos': 2,
            'calidad_maxima': 'Full HD',
            'es_activo': True
        },
        {
            'nombre': 'VIP',
            'tipo': 'vip',
            'precio_mensual': 19.99,
            'descripcion': 'Acceso VIP con todos los beneficios',
            'caracteristicas': [
                'Acceso a todo el contenido',
                'Calidad 4K Ultra HD',
                '4 dispositivos simultáneos',
                'Sin anuncios',
                'Descarga offline',
                'Contenido exclusivo',
                'Soporte prioritario'
            ],
            'max_dispositivos': 4,
            'calidad_maxima': '4K Ultra HD',
            'es_activo': True
        }
    ]
    
    # Crear planes
    for plan_data in plans_data:
        plan = PlanSuscripcion.objects.create(**plan_data)
        print(f"✅ Plan creado: {plan.nombre} - ${plan.precio_mensual}/mes")
    
    print(f"\n🎉 ¡Configuración completada!")
    print(f"\n📊 Resumen:")
    print(f"- Usuarios: {Usuario.objects.count()}")
    print(f"- Planes: {PlanSuscripcion.objects.count()}")
    
    print(f"\n🌐 URLs del API:")
    print(f"- Login: http://localhost:5051/api/auth/login/")
    print(f"- Register: http://localhost:5051/api/auth/register/")
    print(f"- Profile: http://localhost:5051/api/auth/profile/")
    print(f"- Plans: http://localhost:5051/api/subscription/plans/")
    
    print(f"\n📱 Para usar la aplicación:")
    print(f"1. Abre la app móvil")
    print(f"2. Toca 'Registrarse'")
    print(f"3. Completa el formulario")
    print(f"4. Inicia sesión con tus credenciales")
    print(f"5. ¡Disfruta del contenido!")

if __name__ == "__main__":
    setup_database()
