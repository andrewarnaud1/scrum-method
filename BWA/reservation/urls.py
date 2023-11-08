from django.urls import path

from reservation import views

app_name = 'reservation'
urlpatterns = [
    # Gestion des restaurants
    path('create_reservation', views.create_reservation, name='create_reservation'),
    path('reservation_list', views.reservation_list, name='reservation_list'),
]
