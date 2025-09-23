from django.urls import path
from cineapp import views
from cineapp.views_jwt import EmailTokenObtainPairView, ProfileView as ProfileStatsView
from cineapp.views_auth import (
    RegisterView, LoginView, LogoutView, ProfileView,  # usamos solo 1 Profile
    PlanesSuscripcionView, SuscripcionUsuarioView,
    CancelarSuscripcionView, HistorialPagosView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

     path("api/tmdb/detalle/<int:movie_id>/", views.tmdb_detalle, name="tmdb_detalle"),
    # ====================
    # Autenticación
    # ====================
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),  # login normal
    path("auth/login-jwt/", EmailTokenObtainPairView.as_view(), name="login_jwt"),  # login con JWT directo
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Perfil de usuario
    path("auth/profile/", ProfileView.as_view(), name="profile"),              # Perfil básico
    path("auth/profile-stats/", ProfileStatsView.as_view(), name="profile_stats"),  # Perfil extendido (métricas)

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
    # TMDB
    # ====================
    path("tmdb/populares/", views.tmdb_populares, name="tmdb_populares"),
    path("tmdb/buscar/", views.tmdb_buscar, name="tmdb_buscar"),
    path("tmdb/estrenos/", views.tmdb_estrenos, name="tmdb_estrenos"),
    # ====================
    # Favoritos y Vistos
    # ====================
    path("favoritos/", views.favoritos, name="favoritos"),
    path("favoritos/<int:pk>/", views.favorito_detalle, name="favorito_detalle"),
    path("vistos/", views.vistos, name="vistos"),
    path("vistos/<int:pk>/", views.visto_detalle, name="visto_detalle"),

    # ====================
    # Perfil
    # ====================
    path("profile/update/", views.update_profile, name="update_profile"),

    # ====================
    # Suscripción
    # ====================
    path("subscription/plans/", PlanesSuscripcionView.as_view(), name="planes_suscripcion"),
    path("subscription/", SuscripcionUsuarioView.as_view(), name="suscripcion_usuario"),
    path("subscription/cancel/", CancelarSuscripcionView.as_view(), name="cancelar_suscripcion"),
    path("subscription/payments/", HistorialPagosView.as_view(), name="historial_pagos"),
]
