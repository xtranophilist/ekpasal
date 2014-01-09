from django.template import Library
from django import template
register = Library()

@register.filter
def get_starting_price(objects):
    if len(objects) == 1:
        return objects[0].price
    starting_price = objects[0].price
    iterables = iter(objects)
    next(iterables)
    for obj in iterables:
        if obj.price < starting_price:
            starting_price = obj.price
    return 'Starting from '+ str(starting_price)

