from django.db import models
from django.core.validators import MaxValueValidator

class Avis(models.Model):
    #nom_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    avis_text = models.CharField(max_length=200)
    avis_rate = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=10)],)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)


    def __str__(self):
        return self
