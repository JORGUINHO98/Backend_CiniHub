# 🚀 CineHub Backend - Guía de Configuración

## ✅ Correcciones Implementadas

### 1. **Puertos Corregidos**
- Backend: Puerto `5051` (externo) → `8050` (interno)
- pgAdmin: Puerto `5052` (evita conflicto)

### 2. **Endpoints Agregados**
- `GET/POST /api/favoritos/` - CRUD de favoritos
- `GET/PUT/DELETE /api/favoritos/<id>/` - Detalle de favoritos
- `GET/POST /api/vistos/` - CRUD de vistos
- `GET/PUT/DELETE /api/vistos/<id>/` - Detalle de vistos

### 3. **CORS Configurado**
- Orígenes específicos para desarrollo móvil
- Configuración segura para producción

### 4. **Variables de Entorno**
- API keys movidas a variables de entorno
- Configuración centralizada

## 🛠️ Instrucciones de Instalación

### 1. **Iniciar Backend**
```bash
cd App_Backend-main
docker-compose up -d
```

### 2. **Verificar Funcionamiento**
```bash
# Verificar que el backend esté corriendo
curl http://localhost:5051/api/

# Verificar base de datos
docker-compose logs db
```

### 3. **Configurar Base de Datos**
```bash
# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

## 🔧 Configuración del Frontend

### 1. **Instalar Dependencias**
```bash
cd Cine.Front
npm install
```

### 2. **Configurar Variables de Entorno**
Crear archivo `.env` en `Cine.Front/`:
```env
EXPO_PUBLIC_API_URL=http://localhost:5051/api
EXPO_PUBLIC_TMDB_API_KEY=tu_api_key_aqui
```

### 3. **Iniciar Frontend**
```bash
npm start
```

## 🌐 URLs Importantes

- **Backend API**: http://localhost:5051/api/
- **Admin Django**: http://localhost:5051/admin/
- **pgAdmin**: http://localhost:5052/
- **Frontend**: http://localhost:8081 (Expo)

## 🔑 Credenciales por Defecto

- **pgAdmin**: administrador@admin.com / admin12345
- **Base de datos**: cinehub_db / cinehub_user / cinehub_pass

## ⚠️ Notas Importantes

1. **Puerto 5051**: Ahora mapea correctamente al backend
2. **CORS**: Configurado para desarrollo móvil
3. **API Keys**: Usar variables de entorno en producción
4. **Base de datos**: PostgreSQL en Docker

## 🐛 Solución de Problemas

### Error de Conexión
```bash
# Verificar que los contenedores estén corriendo
docker-compose ps

# Ver logs del backend
docker-compose logs web
```

### Error de CORS
- Verificar que el frontend use `http://localhost:5051/api`
- Revisar configuración de CORS en `settings.py`

### Error de Base de Datos
```bash
# Reiniciar base de datos
docker-compose down
docker-compose up -d db
docker-compose exec web python manage.py migrate
```
