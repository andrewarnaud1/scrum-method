from django.urls import path

from core import views

app_name = 'core'
urlpatterns = [
    # Gestion des utilisateurs
    path('creation-utilisateur', views.CreateUtilisateurView.as_view(), name='creation-utilisateur'),
    path('modification-utilisateur/<int:pk>', views.EditUtilisateurView.as_view(), name='modification-utilisateur'),
    path('liste-utilisateur', views.ListUtilisateurView.as_view(), name='liste-utilisateur'),
    path('delete-utilisateur/<int:pk>', views.DeleteUtilisateurView.as_view(), name="delete-utilisateur"),

    # Suppression d'un objet, peu importe sa classe (préciser le module, la classe et l'url de retour en query)
    path('suppression/<int:pk>', views.DeleteObjectView.as_view(), name='suppression'),
]
