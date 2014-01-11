import json
from django.db.models import Model
from django.template import Library
from django import template
from django.utils.safestring import mark_safe
from app.libr import json_handler

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
    return 'Starting from ' + str(starting_price)


@register.filter
def parse_availability(availability):
    if availability == 0:
        return 'In Stock'
    elif availability == 0:
        return 'Out of Stock'
    else:
        return availability


@register.filter
def jsonify(object):
    # if isinstance(object, QuerySet):
    #     return serializers.serialize('json', object)
    if isinstance(object, Model):
        model_dict = object.__dict__
        del model_dict['_state']
        return mark_safe(json.dumps(model_dict))
    return mark_safe(json.dumps(object, default=json_handler))