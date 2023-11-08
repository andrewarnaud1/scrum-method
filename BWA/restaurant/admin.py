from django.contrib import admin

from restaurant.models import Restaurant


# Gestion de l'administration des Fournisseurs.


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    search_fields = ['raison_sociale', 'adresse', 'email']