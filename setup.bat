@echo off
echo 🎬 Configurando CineHub Backend...

REM Detener contenedores existentes
echo 🛑 Deteniendo contenedores existentes...
docker-compose down

REM Construir y levantar los contenedores
echo 🔨 Construyendo y levantando contenedores...
docker-compose up --build -d

REM Esperar a que la base de datos esté lista
echo ⏳ Esperando a que la base de datos esté lista...
timeout /t 15 /nobreak > nul

REM Ejecutar migraciones
echo 📊 Ejecutando migraciones de Django...
docker-compose exec web python manage.py migrate

echo ✅ ¡CineHub Backend configurado exitosamente!
echo 🌐 Backend disponible en: http://localhost:8050
echo 🗄️  PgAdmin disponible en: http://localhost:5050
echo 📊 Redis disponible en: localhost:6379
echo.
echo Para ver los logs: docker-compose logs -f
echo Para detener: docker-compose down
pause
