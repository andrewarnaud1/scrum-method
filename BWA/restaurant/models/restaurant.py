from django.db import models


class Restaurant(models.Model):
    raison_sociale = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    description = models.TextField()
    restaurateur = models.ForeignKey('utilisateur.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.raison_sociale


class Adresse(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    street = models.CharField(max_length=200)
    zip = models.IntegerField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=80)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.restaurant.nom},{self.street}, {self.city} ({self.country})"
