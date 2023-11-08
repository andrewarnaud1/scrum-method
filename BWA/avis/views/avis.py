from django.shortcuts import render, redirect
from avis.models import Avis
from avis.forms import AvisForm

def create_avis(request):
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aviss:avis_list')
    else:
        form = AvisForm()
    return render(request, 'create_avis.html', {'form': form})

def avis_list(request):
    aviss = Avis.objects.all()
    return render(request, 'list_avis.html', {'aviss': aviss})
