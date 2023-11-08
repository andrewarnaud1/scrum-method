from django.urls import path

from avis import views

app_name = 'avis'
urlpatterns = [
    path('create_avis', views.create_avis, name='create_avis'),
    path('avis_list', views.avis_list, name='avis_list'),
]
