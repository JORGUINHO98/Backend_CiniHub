# CineHub Backend

### Levantar servicios
```bash
docker-compose up -d --build
```

### Crear superusuario
```bash
docker-compose exec web python manage.py createsuperuser
```

El backend estará disponible en: [http://localhost:8050/api/](http://localhost:8050/api/)
