from django.urls import path
from cineapp import views
from cineapp.views_jwt import EmailTokenObtainPairView, ProfileView
from cineapp.views_auth import (
    RegisterView, LoginView, LogoutView,
    PlanesSuscripcionView, SuscripcionUsuarioView,
    CancelarSuscripcionView, HistorialPagosView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Auth
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/login-jwt/", EmailTokenObtainPairView.as_view(), name="login-jwt"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),

    # Usuarios
    path("usuarios/", views.usuarios, name="usuarios"),
    path("usuarios/<int:pk>/", views.usuario_detalle, name="usuario_detalle"),

    # Películas
    path("peliculas/", views.peliculas, name="peliculas"),

    # TMDB
    path("tmdb/populares/", views.tmdb_populares, name="tmdb_populares"),
    path("tmdb/buscar/", views.tmdb_buscar, name="tmdb_buscar"),

    # Favoritos y vistos
    path("favoritos/", views.favoritos, name="favoritos"),
    path("vistos/", views.vistos, name="vistos"),

    # Perfil
    path("profile/update/", views.update_profile, name="update_profile"),

    # Suscripción
    path("subscription/plans/", PlanesSuscripcionView.as_view(), name="planes_suscripcion"),
    path("subscription/", SuscripcionUsuarioView.as_view(), name="suscripcion_usuario"),
    path("subscription/cancel/", CancelarSuscripcionView.as_view(), name="cancelar_suscripcion"),
    path("subscription/payments/", HistorialPagosView.as_view(), name="historial_pagos"),
]
