from django.shortcuts import render
from store.models import Category, Product
from app.libr import markup_or_json
from haystack.query import SearchQuerySet

def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'list_categories.html', {'categories': categories})


@markup_or_json('base.html')
def view_category(request, slug):
    category = Category.objects.get(slug=slug)
    products = []
    for product in category.products.all():
        products.append(product.serialize())
    for descendant in category.get_descendants():
        for product in descendant.products.all():
            products.append(product.serialize())
    data = {
        'products': products,
        'type': 'category',
        'source': category.serialize(),
        'title': category.name,
    }
    return data


@markup_or_json('base.html')
def view_product(request, slug):
    product = Product.objects.get(slug=slug)
    data = {
        'product': product.serialize(),
        'type': 'product',
        'title': product.name,
    }
    return data

@markup_or_json('base.html')
def search(request, keyword):
    print keyword
    results = SearchQuerySet().filter(content=keyword)
    import pdb
    pdb.set_trace()