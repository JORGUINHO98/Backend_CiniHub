from django.urls import path
from cineapp import views
from cineapp.views_jwt import EmailTokenObtainPairView, ProfileView
from cineapp.views_auth import (RegisterView, PlanesSuscripcionView, SuscripcionUsuarioView, 
                               CancelarSuscripcionView, HistorialPagosView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # ====================
    # JWT Authentication (login con email)
    # ====================
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", EmailTokenObtainPairView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),

    # ====================
    # Usuarios
    # ====================
    path("usuarios/", views.usuarios, name="usuarios"),
    path("usuarios/<int:pk>/", views.usuario_detalle, name="usuario_detalle"),

    # ====================
    # Películas
    # ====================
    path("peliculas/", views.peliculas, name="peliculas"),
    path("peliculas/<int:pk>/", views.pelicula_detalle, name="pelicula_detalle"),

    # ====================
    # TMDb
    # ====================
    path("tmdb/populares/", views.tmdb_populares, name="tmdb_populares"),
    path("tmdb/buscar/", views.tmdb_buscar, name="tmdb_buscar"),
    # path("tmdb/guardar/", views.tmdb_guardar, name="tmdb_guardar"),
    # path("tmdb/guardar-favorito/<int:usuario_id>/", views.tmdb_guardar_favorito, name="tmdb_guardar_favorito"),
    # path("tmdb/quitar-favorito/<int:usuario_id>/<int:pelicula_id>/", views.tmdb_quitar_favorito, name="tmdb_quitar_favorito"),

    # ====================
    # Favoritos
    # ====================
    path("favoritos/", views.favoritos, name="favoritos"),
    path("favoritos/<int:pk>/", views.favorito_detalle, name="favorito_detalle"),

    # ====================
    # Vistos
    # ====================
    path("vistos/", views.vistos, name="vistos"),
    path("vistos/<int:pk>/", views.visto_detalle, name="visto_detalle"),

    # ====================
    # Perfil de usuario
    # ====================
    path("profile/update/", views.update_profile, name="update_profile"),

    # ====================
    # Suscripciones
    # ====================
    path("subscription/plans/", PlanesSuscripcionView.as_view(), name="planes_suscripcion"),
    path("subscription/", SuscripcionUsuarioView.as_view(), name="suscripcion_usuario"),
    path("subscription/cancel/", CancelarSuscripcionView.as_view(), name="cancelar_suscripcion"),
    path("subscription/payments/", HistorialPagosView.as_view(), name="historial_pagos"),
]
