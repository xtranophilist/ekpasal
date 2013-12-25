from django.contrib import admin
from store.models import Store, Vendor, Brand, Category, Currency, Product

admin.site.register(Store)
admin.site.register(Vendor)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Currency)
admin.site.register(Product)

