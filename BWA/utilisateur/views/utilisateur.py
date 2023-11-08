from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignUpForm

def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecte automatiquement l'utilisateur après l'inscription
            # Rediriger vers une page appropriée
            return redirect('home')
    else:
        form = UserSignUpForm()
    return render(request, 'signup.html', {'form': form})
