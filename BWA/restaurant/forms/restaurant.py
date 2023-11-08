from django import forms
from django.forms import inlineformset_factory
from restaurant.models import Restaurant, Adresse

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = "__all__"

    def clean(self):
        new_raison_sociale = self.cleaned_data.get("raison_sociale")

<<<<<<< HEAD
        if Restaurant.objects.filter(
            raison_sociale=new_raison_sociale
        ).exists():
            raise forms.ValidationError("Restaurant existant")

AdresseFormSet = inlineformset_factory(Restaurant, Adresse, fields=('street', 'zip', 'city', 'country', 'lat', 'lng'))
=======
        errors = {}

        if Restaurant.objects.filter(addresse=new_addresse).exists():
            errors['addresse'] = 'Un restaurant avec cette adresse existe déjà.'

        if Restaurant.objects.filter(raison_sociale=new_raison_sociale, addresse=new_addresse).exists():
            errors['raison_sociale'] = 'Ce restaurant existe déjà.'

        if errors:
            raise forms.ValidationError(errors)
>>>>>>> c03913b4420b10b4657dfb6a856eb245e1ebfb58
