from django.urls import path

from restaurant import views

app_name = 'restaurant'
urlpatterns = [
    # Gestion des restaurants
    path('create_restaurant', views.create_restaurant, name='create_restaurant'),
    path('restaurant_list', views.restaurant_list, name='restaurant_list'),
]
