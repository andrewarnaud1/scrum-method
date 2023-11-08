from django.shortcuts import render, redirect
from restaurant.models import Restaurant
from restaurant.forms import RestaurantForm

def create_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant:restaurant_list')
    else:
        form = RestaurantForm()
    return render(request, 'create.html', {'form': form})

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'list.html', {'restaurants': restaurants})
