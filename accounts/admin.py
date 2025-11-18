from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            'Información personal',
            {
                'fields': (
                    'rut',
                    'maternal_last_name',
                    'age',
                    'occupation',
                    'sex',
                    'phone',
                    'city',
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Datos del perfil',
            {
                'fields': (
                    'rut',
                    'maternal_last_name',
                    'age',
                    'occupation',
                    'sex',
                    'phone',
                    'city',
                )
            },
        ),
    )
    list_display = ['username', 'rut', 'email', 'is_staff', 'profile_completed']
    search_fields = ['username', 'email', 'rut']
