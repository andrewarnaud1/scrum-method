from django.urls import path
from .views import signup

app_name = 'utilisateur'

urlpatterns = [
    path('signup/', signup, name='signup'),
]

