from django.shortcuts import render, redirect
from restaurant.models import Restaurant
from restaurant.forms import RestaurantForm, AdresseFormSet
from django.forms import inlineformset_factory
from restaurant.models import Restaurant, Adresse
from django.forms import inlineformset_factory


def create_restaurant(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        adresse_formset = AdresseFormSet(request.POST, instance=Restaurant())  # Utilisez une instance vide de Restaurant ici
        if form.is_valid() and adresse_formset.is_valid():
            restaurant = form.save()
            adresse_formset.instance = restaurant
            adresse_formset.save()
            return redirect("restaurant:restaurant_list")
    else:
        form = RestaurantForm()
        adresse_formset = AdresseFormSet(instance=Restaurant())  # Utilisez une instance vide de Restaurant ici
    return render(
        request,
        "create.html",
        {"form": form, "adresse_formset": adresse_formset},
    )


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, "list.html", {"restaurants": restaurants})
