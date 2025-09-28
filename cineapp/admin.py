from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # type: ignore

from .models import Permiso, Rol, Usuario, Favorito, Visto


@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre",)


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    filter_horizontal = ("permisos",)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ("id", "email", "nombre", "is_active", "is_staff")
    search_fields = ("email", "nombre")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información Personal", {"fields": ("nombre",)}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nombre", "password1", "password2", "is_active", "is_staff", "is_superuser")},
        ),
    )


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "get_pelicula", "lista_de_pelicula")
    search_fields = ("usuario__email", "pelicula__titulo")

    def get_pelicula(self, obj):
        return obj.pelicula.titulo if obj.pelicula else "-"
    get_pelicula.short_description = "Película"


@admin.register(Visto)
class VistoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "get_titulo", "calificacion", "fecha_visto", "porcentaje_visto")
    search_fields = ("usuario__email", "pelicula__titulo")
    list_filter = ("fecha_visto", "calificacion")

    def get_titulo(self, obj):
        return obj.pelicula.titulo if obj.pelicula else "-"
    get_titulo.short_description = "Título"
