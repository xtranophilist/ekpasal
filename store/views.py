from django.shortcuts import render
from store.models import Category, Product

def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'list_categories.html', {'categories': categories})

def view_category(request, slug):
    category = Category.objects.get(slug=slug)
    products = []
    for product in category.products.all():
        products.append(product.serialize())
    data = {
        'products': products,
        'type': 'category',
        'source': category.serialize()
    }
    return render(request, 'base.html', {'data': data})


def view_product(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'view_product.html', {'product': product})