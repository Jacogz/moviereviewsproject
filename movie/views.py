from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

# Create your views here.
def home(request):
    searchTerm = request.GET.get('searchMovie')
    movies = Movie.objects.all()
    return render(request, 'home.html', {'name': 'Jacobo', 'movies': movies})

def about(request):
    return render(request, 'about.html')
