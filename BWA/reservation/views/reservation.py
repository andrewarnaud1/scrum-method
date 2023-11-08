from django.shortcuts import render, redirect
from reservation.models import Reservation
from reservation.forms import ReservationForm

def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservations:reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'create_reservation.html', {'form': form})

def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'list_reservation.html', {'reservations': reservations})
