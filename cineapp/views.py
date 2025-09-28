# cineapp/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import get_object_or_404
import requests

from .models import Pelicula, Usuario, Favorito, Visto
from .serializers import UsuarioRegisterSerializer, UsuarioSerializer

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

def normalize_movie_from_model(pelicula: Pelicula):
    return {
        "id": pelicula.tmdb_id,
        "title": pelicula.titulo,
        "overview": pelicula.descripcion,
        "poster_path": pelicula.poster,
        "release_date": pelicula.fecha_lanzamiento,
        "vote_average": 0,
        "genre_ids": [],
    }

# ============================
# Películas (CRUD local)
# ============================

@api_view(["GET", "POST"])
def peliculas(request):
    if request.method == "GET":
        peliculas = Pelicula.objects.all()
        data = [normalize_movie_from_model(p) for p in peliculas]
        return Response(data)

    elif request.method == "POST":
        data = request.data
        pelicula = Pelicula.objects.create(
            tmdb_id=data.get("id"),
            titulo=data.get("title"),
            descripcion=data.get("overview"),
            poster=data.get("poster_path"),
            fecha_lanzamiento=data.get("release_date"),
        )
        return Response(normalize_movie_from_model(pelicula), status=201)


@api_view(["GET", "PUT", "DELETE"])
def pelicula_detalle(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)

    if request.method == "GET":
        return Response(normalize_movie_from_model(pelicula))

    elif request.method == "PUT":
        data = request.data
        pelicula.titulo = data.get("title", pelicula.titulo)
        pelicula.descripcion = data.get("overview", pelicula.descripcion)
        pelicula.poster = data.get("poster_path", pelicula.poster)
        pelicula.fecha_lanzamiento = data.get("release_date", pelicula.fecha_lanzamiento)
        pelicula.save()
        return Response(normalize_movie_from_model(pelicula))

    elif request.method == "DELETE":
        pelicula.delete()
        return Response({"mensaje": "Pelicula eliminada"}, status=204)

# ============================
# Usuarios
# ============================

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def usuarios(request):
    if request.method == "GET":
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"error": "Solo administradores pueden listar usuarios"}, status=403)
        usuarios = Usuario.objects.all()
        return Response(UsuarioSerializer(usuarios, many=True).data)

    elif request.method == "POST":
        serializer = UsuarioRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UsuarioSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def usuario_detalle(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)

    if request.user != usuario and not request.user.is_staff:
        return Response({"error": "No autorizado"}, status=403)

    if request.method == "GET":
        return Response(UsuarioSerializer(usuario).data)

    elif request.method == "PUT":
        serializer = UsuarioRegisterSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UsuarioSerializer(usuario).data)
        return Response(serializer.errors, status=400)

    elif request.method == "DELETE":
        usuario.delete()
        return Response({"mensaje": "Usuario eliminado"}, status=204)

# ============================
# TMDb - Populares, Buscar, Detalle, Estrenos
# ============================

@api_view(["GET"])
@permission_classes([AllowAny])
def tmdb_populares(request):
    cache_key = "tmdb_populares"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {"api_key": TMDB_API_KEY, "language": "es-ES", "page": 1}
    res = requests.get(url, params=params, timeout=10)
    if res.status_code == 200:
        data = res.json()
        movies = [normalize_movie(m) for m in data.get("results", [])]
        cache.set(cache_key, movies, 3600)
        return Response(movies)
    return Response({"error": "No se pudo obtener"}, status=400)


@api_view(["GET"])
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

    url = f"{TMDB_BASE_URL}/search/movie"
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
@permission_classes([AllowAny])
def tmdb_detalle(request, movie_id):
    try:
        detalle_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        detalle_params = {"api_key": TMDB_API_KEY, "language": "es-ES"}
        detalle_res = requests.get(detalle_url, params=detalle_params).json()

        creditos_url = f"{TMDB_BASE_URL}/movie/{movie_id}/credits"
        creditos_params = {"api_key": TMDB_API_KEY, "language": "es-ES"}
        creditos_res = requests.get(creditos_url, params=creditos_params).json()

        actores = [actor["name"] for actor in creditos_res.get("cast", [])[:5]]
        director = next((c["name"] for c in creditos_res.get("crew", []) if c["job"] == "Director"), "Desconocido")

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


@api_view(["GET"])
@permission_classes([AllowAny])
def tmdb_estrenos(request):
    cache_key = "tmdb_estrenos"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    url = f"{TMDB_BASE_URL}/movie/now_playing"
    params = {"api_key": TMDB_API_KEY, "language": "es-ES", "page": 1}
    res = requests.get(url, params=params, timeout=10)
    if res.status_code == 200:
        data = res.json()
        movies = [normalize_movie(m) for m in data.get("results", [])]
        cache.set(cache_key, movies, 3600)
        return Response(movies)
    return Response({"error": "No se pudo obtener"}, status=400)

# ============================
# Favoritos
# ============================

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def favoritos(request):
    if request.method == "GET":
        favoritos = Favorito.objects.filter(usuario=request.user).select_related("pelicula")
        data = [
            {
                "id": fav.pk,
                "movie": normalize_movie_from_model(fav.pelicula),
            }
            for fav in favoritos
        ]
        return Response(data)

    elif request.method == "POST":
        data = request.data
        tmdb_id = data.get("tmdb_id") or data.get("id")
        if not tmdb_id:
            return Response({"error": "Se requiere tmdb_id"}, status=400)

        pelicula, _ = Pelicula.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                "titulo": data.get("title", ""),
                "descripcion": data.get("overview", ""),
                "poster": data.get("poster_path"),
                "fecha_lanzamiento": data.get("release_date"),
            },
        )
        favorito, created = Favorito.objects.get_or_create(usuario=request.user, pelicula=pelicula)
        if not created:
            return Response(
                {
                    "mensaje": "Ya estaba en favoritos",
                    "id": favorito.pk,
                    "movie": normalize_movie_from_model(pelicula),
                },
                status=200,
            )

        return Response(
            {"id": favorito.pk, "movie": normalize_movie_from_model(pelicula)},
            status=201,
        )


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def favorito_detalle(request, pk):
    try:
        favorito = Favorito.objects.select_related("pelicula").get(pk=pk, usuario=request.user)
    except Favorito.DoesNotExist:
        return Response({"error": "Favorito no encontrado"}, status=404)

    if request.method == "GET":
        return Response({"id": favorito.pk, "movie": normalize_movie_from_model(favorito.pelicula)})

    elif request.method == "DELETE":
        favorito.delete()
        return Response({"mensaje": "Favorito eliminado"}, status=204)


# ============================
# Vistos
# ============================

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def vistos(request):
    if request.method == "GET":
        vistos = Visto.objects.filter(usuario=request.user).select_related("pelicula")
        data = [
            {
                "id": v.pk,
                "movie": normalize_movie_from_model(v.pelicula),
                "calificacion": getattr(v, "calificacion", None),
            }
            for v in vistos
        ]
        return Response(data)

    elif request.method == "POST":
        data = request.data
        tmdb_id = data.get("tmdb_id") or data.get("id")
        if not tmdb_id:
            return Response({"error": "Se requiere tmdb_id"}, status=400)

        pelicula, _ = Pelicula.objects.get_or_create(
            tmdb_id=tmdb_id,
            defaults={
                "titulo": data.get("title", ""),
                "descripcion": data.get("overview", ""),
                "poster": data.get("poster_path"),
                "fecha_lanzamiento": data.get("release_date"),
            },
        )
        visto, created = Visto.objects.get_or_create(usuario=request.user, pelicula=pelicula)
        if not created:
            return Response(
                {
                    "mensaje": "Ya estaba en vistos",
                    "id": visto.pk,
                    "movie": normalize_movie_from_model(pelicula),
                    "calificacion": getattr(visto, "calificacion", None),
                },
                status=200,
            )

        return Response(
            {"id": visto.pk, "movie": normalize_movie_from_model(pelicula), "calificacion": None},
            status=201,
        )


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def visto_detalle(request, pk):
    try:
        visto = Visto.objects.select_related("pelicula").get(pk=pk, usuario=request.user)
    except Visto.DoesNotExist:
        return Response({"error": "Visto no encontrado"}, status=404)

    if request.method == "GET":
        return Response(
            {
                "id": visto.pk,
                "movie": normalize_movie_from_model(visto.pelicula),
                "calificacion": getattr(visto, "calificacion", None),
            }
        )

    elif request.method == "PUT":
        cal = request.data.get("calificacion")
        if cal is not None:
            try:
                visto.calificacion = float(cal)
                visto.save()
            except Exception:
                return Response({"error": "Calificación inválida"}, status=400)

        return Response(
            {
                "id": visto.pk,
                "movie": normalize_movie_from_model(visto.pelicula),
                "calificacion": getattr(visto, "calificacion", None),
            }
        )

    elif request.method == "DELETE":
        visto.delete()
        return Response({"mensaje": "Marcado como visto eliminado"}, status=204)

# ============================
# Update Profile
# ============================

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    data = request.data
    serializer = UsuarioRegisterSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"mensaje": "Perfil actualizado", "usuario": UsuarioSerializer(user).data})
    return Response(serializer.errors, status=400)
