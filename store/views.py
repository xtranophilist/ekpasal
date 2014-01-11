from django.shortcuts import render
from store.models import Category, Product
from app.libr import markup_or_json


def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'list_categories.html', {'categories': categories})


@markup_or_json('base.html')
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
    return data


@markup_or_json('base.html')
def view_product(request, slug):
    product = Product.objects.get(slug=slug)
    data = {
        'product': product.serialize(),
        'type': 'product',
    }
    return data