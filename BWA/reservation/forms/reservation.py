from reservation.models import Reservation
from django import forms


class ReservationForm(forms.ModelForm):
    date_reservation = forms.DateField(
        label='Date',
        widget=forms.SelectDateWidget()
    )
    class Meta:
        model = Reservation
        fields = "__all__"
