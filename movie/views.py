from django.shortcuts import render
from django.http import HttpResponse

import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64 

from .models import Movie

# Create your views here.
def home(request):
    searchTerm = request.GET.get('search')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains = searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'name': 'Jacobo', 'movies': movies, 'searchTerm': searchTerm})

def about(request):
    return render(request, 'about.html')

def statistics_view(request): 
    matplotlib.use('Agg') 
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    genres_all = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre')
    genres = [genres.partition(',')[0] for genres in genres_all]
    movie_counts_by_year = {}  
    for year in years:
        if year: 
            movies_in_year = Movie.objects.filter(year=year) 
            movie_counts_by_year[year] = movies_in_year.count()
        else: 
            movies_in_year = Movie.objects.filter(year__isnull=True) 
            year = "None" 
            count = movies_in_year.count() 
            movie_counts_by_year[year] = count
    movie_counts_by_genre = {}
    for genre in genres:
        if genre:
            movies_in_genre = Movie.objects.filter(genre__contains=genre)
            movie_counts_by_genre[genre] = movies_in_genre.count()
        else:
            movies_in_genre = Movie.objects.filter(genre__isnull=True)
            genre = "None"
            count = movies_in_genre.count()
            movie_counts_by_genre[genre] = count
            
    bar_width = 0.5 
    bar_spacing = 0.5  
    bar_positions = range(len(movie_counts_by_year))
    # Crear la gráfica de barras 
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center') 
    # Personalizar la gráfica 
    plt.title('Movies per year') 
    plt.xlabel('Year') 
    plt.ylabel('Number of movies') 
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90) 
    # Ajustar el espaciado entre las barras 
    plt.subplots_adjust(bottom=0.3) 
    # Guardar la gráfica en un objeto BytesIO 
    buffer = io.BytesIO() 
    plt.savefig(buffer, format='png') 
    buffer.seek(0) 
    plt.close() 
     
    # Convertir la gráfica a base64 
    image_png = buffer.getvalue() 
    buffer.close() 
    graphic = base64.b64encode(image_png) 
    graphic = graphic.decode('utf-8') 
    
    
    
    bar_positions = range(len(movie_counts_by_genre))
    # Crear la gráfica de barras 
    plt.bar(bar_positions, movie_counts_by_genre.values(), width=bar_width, align='center') 
    # Personalizar la gráfica 
    plt.title('Movies per genre') 
    plt.xlabel('Genre') 
    plt.ylabel('Number of movies') 
    plt.xticks(bar_positions, movie_counts_by_genre.keys(), rotation=90) 
    # Ajustar el espaciado entre las barras 
    plt.subplots_adjust(bottom=0.3) 
    # Guardar la gráfica en un objeto BytesIO 
    buffer = io.BytesIO() 
    plt.savefig(buffer, format='png') 
    buffer.seek(0) 
    plt.close() 
     
    # Convertir la gráfica a base64 
    image_png2 = buffer.getvalue() 
    buffer.close() 
    graphic2 = base64.b64encode(image_png2) 
    graphic2 = graphic2.decode('utf-8') 
 
    # Renderizar la plantilla statistics.html con la gráfica 
    return render(request, 'statistics.html', {'graphic_moviexyear': graphic, 'graphic_moviexgenre': graphic2}) 

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})