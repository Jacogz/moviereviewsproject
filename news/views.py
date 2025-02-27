from django.shortcuts import render
from .models import News

# Create your views here.
def news(request):
    searchTerm = request.GET.get('search')
    if searchTerm:
        news = News.objects.filter(title__icontains = searchTerm)
    else:
        news = News.objects.all()
    return render(request, 'news.html', {'news': news, 'searchTerm': searchTerm})