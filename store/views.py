from django.shortcuts import render
from store.models import Category, Product

def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'list_categories.html', {'categories': categories})

def view_category(request, slug):
    category = Category.objects.get(slug=slug)
    return render(request, 'view_category.html', {'category': category})


def view_product(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'view_product.html', {'product': product})