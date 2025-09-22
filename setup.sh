#!/bin/bash

# Script de configuración para CineHub Backend
echo "🎬 Configurando CineHub Backend..."

# Detener contenedores existentes
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down

# Limpiar volúmenes si es necesario (descomenta la siguiente línea si quieres empezar desde cero)
# docker-compose down -v

# Construir y levantar los contenedores
echo "🔨 Construyendo y levantando contenedores..."
docker-compose up --build -d

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que la base de datos esté lista..."
sleep 10

# Ejecutar migraciones
echo "📊 Ejecutando migraciones de Django..."
docker-compose exec web python manage.py migrate

# Crear superusuario (opcional)
echo "👤 ¿Quieres crear un superusuario? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    docker-compose exec web python manage.py createsuperuser
fi

# Poblar datos de ejemplo (opcional)
echo "📝 ¿Quieres poblar datos de ejemplo? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    docker-compose exec web python populate_subscription_plans.py
fi

echo "✅ ¡CineHub Backend configurado exitosamente!"
echo "🌐 Backend disponible en: http://localhost:8050"
echo "🗄️  PgAdmin disponible en: http://localhost:5050"
echo "📊 Redis disponible en: localhost:6379"
echo ""
echo "Para ver los logs: docker-compose logs -f"
echo "Para detener: docker-compose down"
