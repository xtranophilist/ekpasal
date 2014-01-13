from django.shortcuts import render
from store.models import Category, Product
from app.libr import markup_or_json
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'list_categories.html', {'categories': categories})


def filter_items(request, items):
    items_per_page = 12
    page = int(request.GET.get('page') or 1)
    # 1 = in stock only, 0 = all, -1 = out of stock only
    stock = request.GET.get('stock') or 1
    store = request.GET.get('store')
    min_price = request.GET.get('min_price') or 0
    max_price = request.GET.get('max_price') or 100000
    products = []
    filtered_products = items.filter(price__lt=max_price, price__gt=min_price).select_related()
    if store:
        filtered_products = filtered_products.filter(store__name=store)
    if stock == '1' or stock == 1:
        filtered_products = filtered_products.filter(availability__gt=-1)
    elif stock == '-1':
        filtered_products = filtered_products.filter(availability=-1)
    pages = (len(filtered_products) + items_per_page // 2) // items_per_page
    filtered_products = filtered_products[(page - 1) * items_per_page:(page * items_per_page)]
    for product in filtered_products:
        products.append(product.serialize())
    data = {
        'products': products,
        'pages': pages,
    }
    return data


@markup_or_json('base.html')
def view_category(request, slug):
    category = Category.objects.get(slug=slug)
    items = Product.objects.filter(categories=category.get_descendants(include_self=True))
    data = filter_items(request, items)
    data['source'] = category.serialize()
    data['title'] = category.name
    data['type'] = 'category'
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
    products = []
    if keyword == '':
        keyword = request.GET.get('q') or ''
    results = SearchQuerySet().filter(content=keyword)
    for result in results:
        product = Product.objects.get(id=result.pk)
        products.append(product.serialize())
    data = {
        'results': products,
        'type': 'search',
        'title': 'Search: ' + keyword,
        'keyword': keyword,
    }
    return data