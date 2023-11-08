from django import forms
from django.forms import inlineformset_factory
from restaurant.models import Restaurant, Adresse

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = "__all__"

    def clean(self):
        new_raison_sociale = self.cleaned_data.get("raison_sociale")

        if Restaurant.objects.filter(
            raison_sociale=new_raison_sociale
        ).exists():
            raise forms.ValidationError("Restaurant existant")

AdresseFormSet = inlineformset_factory(Restaurant, Adresse, fields=('street', 'zip', 'city', 'country', 'lat', 'lng'))
