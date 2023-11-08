from django.db import models

class Reservation(models.Model):
    #nom_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_reservation = models.DateField()
    heure_reservation = models.TimeField()
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)


    def __str__(self):
        return self
