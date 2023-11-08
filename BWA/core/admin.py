from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.forms import CreateUtilisateurAdminForm, EditUtilisateurAdminForm
from core.models import Utilisateur


# Gestion de l'administration des utilisateurs.
@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    add_form = CreateUtilisateurAdminForm
    form = EditUtilisateurAdminForm
    model = Utilisateur
    fieldsets = (
        (None, {'fields': ('email', 'password', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'is_staff', 'is_active'),
        }),
    )
    list_display = ('pk', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('-is_active', 'email')
    filter_horizontal = ('groups', 'user_permissions')
