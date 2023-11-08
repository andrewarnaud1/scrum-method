from django.db import models

class Restaurant(models.Model):
    raison_sociale = models.CharField(max_length=100)
    addresse = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.raison_sociale
