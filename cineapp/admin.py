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
    list_display = ("id", "usuario", "id_pelicula", "lista_de_pelicula")
    search_fields = ("usuario__email", "id_pelicula")


@admin.register(Visto)
class VistoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "titulo", "calificacion", "fecha_visto", "porcentaje_visto")
    search_fields = ("usuario__email", "titulo")
    list_filter = ("fecha_visto", "calificacion")
