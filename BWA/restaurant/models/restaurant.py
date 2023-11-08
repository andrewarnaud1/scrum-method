from django.db import models

class Restaurant(models.Model):
    raison_sociale = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    description = models.TextField()
    restaurateur = models.ForeignKey('utilisateur.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.raison_sociale
