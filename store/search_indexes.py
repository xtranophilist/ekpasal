import datetime
from haystack import indexes
from store.models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # description = indexes.CharField(model_attr='description')
    created_on = indexes.DateTimeField(model_attr='created_on')
    updated_on = indexes.DateTimeField(model_attr='updated_on')

    def get_model(self):
        return Product