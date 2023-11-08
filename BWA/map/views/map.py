from django.shortcuts import render
from django.http import FileResponse

def map_view(request):
    # Le chemin vers votre fichier HTML
    file_path = "/Users/andrew/scrum-method/BWA/map/templates/map.html"
    
    # Retourner le fichier en tant que réponse
    return FileResponse(open(file_path, 'rb'), content_type='text/html')