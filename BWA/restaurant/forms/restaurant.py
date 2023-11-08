from restaurant.models import Restaurant
from django import forms


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = "__all__"

    def clean(self):
        new_raison_sociale = self.cleaned_data.get("raison_sociale")
        new_addresse = self.cleaned_data.get("addresse")

        errors = {}

        if Restaurant.objects.filter(addresse=new_addresse).exists():
            errors['addresse'] = 'Un restaurant avec cette adresse existe déjà.'

        if Restaurant.objects.filter(raison_sociale=new_raison_sociale, addresse=new_addresse).exists():
            errors['raison_sociale'] = 'Ce restaurant existe déjà.'

        if errors:
            raise forms.ValidationError(errors)
