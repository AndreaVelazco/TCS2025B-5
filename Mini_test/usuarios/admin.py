from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ['correo', 'nombre', 'perfil', 'fecha_registro', 'is_active']
    list_filter = ['perfil', 'is_active', 'fecha_registro']
    search_fields = ['correo', 'nombre']
    ordering = ['-fecha_registro']
    
    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'perfil')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'nombre', 'password1', 'password2', 'perfil'),
        }),
    )