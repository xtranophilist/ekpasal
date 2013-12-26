from django.shortcuts import render
from store.models import Category

def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'list_categories.html', {'categories': categories})
