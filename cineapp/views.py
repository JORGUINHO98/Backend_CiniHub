from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Pelicula, Usuario, Favorito, Visto


from .serializers import UsuarioRegisterSerializer, UsuarioSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = settings.TMDB_API_KEY

# ============================
# Helpers
# ============================
def normalize_movie(movie):
    return {
        "id": movie.get("id"),
        "title": movie.get("title"),
        "overview": movie.get("overview"),
        "poster_path": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
        "release_date": movie.get("release_date"),
        "vote_average": movie.get("vote_average", 0),
        "genre_ids": movie.get("genre_ids", []),
    }

def normalize_user(user: Usuario):
    return {
        "id": user.id,
        "email": user.email,
        "nombre": user.nombre or "",
        "is_active": user.is_active,
        "fecha_registro": user.fecha_registro,
    }

# ============================
# CRUD Película (local DB)
# ============================
@api_view(['GET', 'POST'])
def peliculas(request):
    if request.method == 'GET':
        peliculas = Pelicula.objects.all()
        data = [
            {
                "id": p.tmdb_id,
                "title": p.titulo,
                "overview": p.descripcion,
                "poster_path": p.poster,
                "release_date": p.fecha_lanzamiento,
                "vote_average": 0,
                "genre_ids": []
            }
            for p in peliculas
        ]
        return Response(data)

    elif request.method == 'POST':
        data = request.data
        pelicula = Pelicula.objects.create(
            tmdb_id=data.get("id"),
            titulo=data.get("title"),
            descripcion=data.get("overview"),
            poster=data.get("poster_path"),
            fecha_lanzamiento=data.get("release_date")
        )
        return Response(normalize_movie(data), status=201)


@api_view(['GET', 'PUT', 'DELETE'])
def pelicula_detalle(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)

    if request.method == 'GET':
        data = {
            "id": pelicula.tmdb_id,
            "title": pelicula.titulo,
            "overview": pelicula.descripcion,
            "poster_path": pelicula.poster,
            "release_date": pelicula.fecha_lanzamiento,
            "vote_average": 0,
            "genre_ids": []
        }
        return Response(data)

    elif request.method == 'PUT':
        data = request.data
        pelicula.titulo = data.get("title", pelicula.titulo)
        pelicula.descripcion = data.get("overview", pelicula.descripcion)
        pelicula.poster = data.get("poster_path", pelicula.poster)
        pelicula.fecha_lanzamiento = data.get("release_date", pelicula.fecha_lanzamiento)
        pelicula.save()

        return Response({
            "id": pelicula.tmdb_id,
            "title": pelicula.titulo,
            "overview": pelicula.descripcion,
            "poster_path": pelicula.poster,
            "release_date": pelicula.fecha_lanzamiento,
            "vote_average": 0,
            "genre_ids": []
        })

    elif request.method == 'DELETE':
        pelicula.delete()
        return Response({"mensaje": "Pelicula eliminada"}, status=204)

# ============================
# CRUD Usuario
# ============================
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def usuarios(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        return Response(UsuarioSerializer(usuarios, many=True).data)

    elif request.method == 'POST':
        serializer = UsuarioRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UsuarioSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def usuario_detalle(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)

    if request.method == 'GET':
        return Response(UsuarioSerializer(usuario).data)

    elif request.method == 'PUT':
        serializer = UsuarioRegisterSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UsuarioSerializer(usuario).data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        usuario.delete()
        return Response({"mensaje": "Usuario eliminado"}, status=204)

# ============================
# TMDb - Populares
# ============================
@api_view(['GET'])
@permission_classes([AllowAny])
def tmdb_populares(request):
    cache_key = "tmdb_populares"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    url = "https://api.themoviedb.org/3/movie/popular"
    params = {"api_key": TMDB_API_KEY, "language": "es-ES", "page": 1}
    res = requests.get(url, params=params, timeout=10)
    if res.status_code == 200:
        data = res.json()
        movies = [normalize_movie(m) for m in data.get("results", [])]
        cache.set(cache_key, movies, 3600)
        return Response(movies)
    return Response({"error": "No se pudo obtener"}, status=400)

# ============================
# TMDb - Buscar
# ============================
@api_view(['GET'])
@permission_classes([AllowAny])
def tmdb_buscar(request):
    query = request.GET.get("q", "").strip()
    page = request.GET.get("page", "1")

    if not query or len(query) < 2:
        return Response({"error": "Debes enviar ?q con al menos 2 caracteres"}, status=400)

    cache_key = f"tmdb_search_{query}_{page}"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "language": "es-ES", "query": query, "page": page}
    res = requests.get(url, params=params, timeout=10)
    if res.status_code == 200:
        data = res.json()
        movies = [normalize_movie(m) for m in data.get("results", [])]
        result = {
            "results": movies,
            "total_pages": data.get("total_pages", 1),
            "total_results": data.get("total_results", 0),
            "page": int(page),
        }
        cache.set(cache_key, result, 1800)
        return Response(result)
    return Response({"error": "No se pudo obtener"}, status=400)


@api_view(["GET"])
def tmdb_detalle(request, movie_id):
    """Obtiene detalles + créditos (actores/director) de una película"""
    try:
        # Detalles básicos
        detalle_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        detalle_params = {"api_key": TMDB_API_KEY, "language": "es-ES"}
        detalle_res = requests.get(detalle_url, params=detalle_params).json()

        # Créditos (cast y crew)
        creditos_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
        creditos_params = {"api_key": TMDB_API_KEY, "language": "es-ES"}
        creditos_res = requests.get(creditos_url, params=creditos_params).json()

        # Actores principales (máx 5)
        actores = [actor["name"] for actor in creditos_res.get("cast", [])[:5]]

        # Director
        director = next(
            (c["name"] for c in creditos_res.get("crew", []) if c["job"] == "Director"),
            "Desconocido"
        )

        data = {
            "id": detalle_res.get("id"),
            "titulo": detalle_res.get("title"),
            "descripcion": detalle_res.get("overview"),
            "poster": f"https://image.tmdb.org/t/p/w500{detalle_res.get('poster_path')}" if detalle_res.get("poster_path") else None,
            "fecha_lanzamiento": detalle_res.get("release_date"),
            "duracion": detalle_res.get("runtime"),
            "generos": [g["name"] for g in detalle_res.get("genres", [])],
            "actores": actores,
            "director": director,
        }

        return Response(data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
# ============================
# Favoritos
# ============================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def favoritos(request):
    if request.method == 'GET':
        favoritos = Favorito.objects.filter(usuario=request.user).select_related("pelicula")
        data = [
            {
                "id": fav.pelicula.tmdb_id,
                "title": fav.pelicula.titulo,
                "overview": fav.pelicula.descripcion,
                "poster_path": fav.pelicula.poster,
                "release_date": fav.pelicula.fecha_lanzamiento,
                "vote_average": 0,
                "genre_ids": []
            }
            for fav in favoritos
        ]
        return Response(data)

    elif request.method == 'POST':
        data = request.data
        tmdb_id = data.get("tmdb_id")
        if not tmdb_id:
            return Response({"error": "Se requiere tmdb_id"}, status=400)

        pelicula, _ = Pelicula.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                "titulo": data.get("title", ""),
                "descripcion": data.get("overview", ""),
                "poster": data.get("poster_path"),
                "fecha_lanzamiento": data.get("release_date"),
            }
        )
        favorito, created = Favorito.objects.get_or_create(usuario=request.user, pelicula=pelicula)
        if not created:
            return Response({"mensaje": "Ya estaba en favoritos"}, status=200)

        return Response({
            "id": pelicula.tmdb_id,
            "title": pelicula.titulo,
            "overview": pelicula.descripcion,
            "poster_path": pelicula.poster,
            "release_date": pelicula.fecha_lanzamiento,
            "vote_average": 0,
            "genre_ids": []
        }, status=201)


# ============================
# Vistos
# ============================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def vistos(request):
    if request.method == 'GET':
        vistos = Visto.objects.filter(usuario=request.user).select_related("pelicula")
        data = [
            {
                "id": v.pelicula.tmdb_id,
                "title": v.pelicula.titulo,
                "overview": v.pelicula.descripcion,
                "poster_path": v.pelicula.poster,
                "release_date": v.pelicula.fecha_lanzamiento,
                "vote_average": 0,
                "genre_ids": []
            }
            for v in vistos
        ]
        return Response(data)

    elif request.method == 'POST':
        data = request.data
        tmdb_id = data.get("tmdb_id")
        if not tmdb_id:
            return Response({"error": "Se requiere tmdb_id"}, status=400)

        pelicula, _ = Pelicula.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                "titulo": data.get("title", ""),
                "descripcion": data.get("overview", ""),
                "poster": data.get("poster_path"),
                "fecha_lanzamiento": data.get("release_date"),
            }
        )
        visto, created = Visto.objects.get_or_create(usuario=request.user, pelicula=pelicula)
        if not created:
            return Response({"mensaje": "Ya estaba en vistos"}, status=200)

        return Response({
            "id": pelicula.tmdb_id,
            "title": pelicula.titulo,
            "overview": pelicula.descripcion,
            "poster_path": pelicula.poster,
            "release_date": pelicula.fecha_lanzamiento,
            "vote_average": 0,
            "genre_ids": []
        }, status=201)
        
# ============================
# Favorito detalle
# ============================
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def favorito_detalle(request, pk):
    try:
        favorito = Favorito.objects.select_related("pelicula").get(pk=pk, usuario=request.user)
    except Favorito.DoesNotExist:
        return Response({"error": "Favorito no encontrado"}, status=404)

    if request.method == 'GET':
        data = {
            "id": favorito.pelicula.tmdb_id,
            "title": favorito.pelicula.titulo,
            "overview": favorito.pelicula.descripcion,
            "poster_path": favorito.pelicula.poster,
            "release_date": favorito.pelicula.fecha_lanzamiento,
            "vote_average": 0,
            "genre_ids": []
        }
        return Response(data)

    elif request.method == 'DELETE':
        favorito.delete()
        return Response({"mensaje": "Favorito eliminado"}, status=204)


# ============================
# Visto detalle
# ============================
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def visto_detalle(request, pk):
    try:
        visto = Visto.objects.select_related("pelicula").get(pk=pk, usuario=request.user)
    except Visto.DoesNotExist:
        return Response({"error": "Visto no encontrado"}, status=404)

    if request.method == 'GET':
        data = {
            "id": visto.pelicula.tmdb_id,
            "title": visto.pelicula.titulo,
            "overview": visto.pelicula.descripcion,
            "poster_path": visto.pelicula.poster,
            "release_date": visto.pelicula.fecha_lanzamiento,
            "vote_average": 0,
            "genre_ids": []
        }
        return Response(data)

    elif request.method == 'DELETE':
        visto.delete()
        return Response({"mensaje": "Marcado como visto eliminado"}, status=204)

# ============================
# Update Profile
# ============================
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data

    serializer = UsuarioRegisterSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Perfil actualizado", "usuario": UsuarioSerializer(user).data})
    return Response(serializer.errors, status=400)
# ============================
# TMDb - Estrenos (now_playing)
# ============================
@api_view(['GET'])
@permission_classes([AllowAny])
def tmdb_estrenos(request):
    cache_key = "tmdb_estrenos"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    url = "https://api.themoviedb.org/3/movie/now_playing"
    params = {"api_key": TMDB_API_KEY, "language": "es-ES", "page": 1}
    res = requests.get(url, params=params, timeout=10)
    if res.status_code == 200:
        data = res.json()
        movies = [normalize_movie(m) for m in data.get("results", [])]
        cache.set(cache_key, movies, 3600)
        return Response(movies)
    return Response({"error": "No se pudo obtener"}, status=400)
