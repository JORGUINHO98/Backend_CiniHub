-- Script de inicialización para CineHub Database
-- Este archivo se ejecuta automáticamente cuando se crea la base de datos

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Configurar la base de datos para UTF-8
SET client_encoding = 'UTF8';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE cinehub_db TO cinehub_user;

-- Configurar timezone
SET timezone = 'UTC';

-- Mensaje de confirmación
SELECT 'CineHub Database initialized successfully!' as message;
