import datetime
from haystack import indexes
from store.models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # description = indexes.CharField(model_attr='description')
    created_on = indexes.DateTimeField(model_attr='created_on')
    updated_on = indexes.DateTimeField(model_attr='updated_on')
    price = indexes.FloatField(model_attr='price')
    availability = indexes.IntegerField(model_attr='availability')
    store = indexes.CharField(model_attr='store__name')

    def get_model(self):
        return Product