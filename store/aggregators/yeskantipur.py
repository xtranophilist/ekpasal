__author__ = 'xtranophilist'
from lxml import html
from lxml.etree import tostring
import re

from store.models import Product, Category, Store, ProductInfo, Currency, Image


class Yeskantipur():
    name = 'YesKantipur'

    def __init__(self):
        self.store = Store.objects.get(name=self.name)
        self.currency = Currency.objects.get(name='NPR')

    root_url = 'http://www.yeskantipur.com'
    # root_url = 'http://localhost/yk'

    category_mapping = {
        'Gents': 'Men',
        'Ladies': 'Women',
        'Sun Glasses': 'Eyewear',
        'Fiction': 'Fiction',
        'Biography & Autobiography': 'Biography',
        'Politics & History': 'Politics & History',
        'Business Management': 'Business',
        'Children': 'Children',
        'Music': 'Music',
        'Economics': 'Economics',
        'Novels': 'Fiction',
        'Nepali': 'Nepali',
        'Mobiles': 'Mobile',
        'Desktops': 'Desktop Computers',
        'Laptops & Notebooks': 'Laptops',
        'Tablets': 'Tablets',
        'Television': 'Television',
        'Monitors': 'Monitors',
        'Cameras': 'Camera',
        'Shoes': 'Shoes',
        'Bags': 'Bags',
        'Jewelry': 'Jewelry',
        'Toys': 'Kids & Toys',
        'Bouquets & Flowers': 'Flowers',
        'Cakes': 'Cakes',
    }

    def mine(self):
        print 'Mining for ' + self.name
        root_page = html.parse(self.root_url)
        root_category_elements = root_page.xpath('//*[@id="column-left"]//ul[@id="navigation"]/li')
        self.parse_category_tree(root_category_elements)

    def parse_category_tree(self, tree):
        for el in tree:
            category_link_list = el.xpath('./a[1]')
            if len(category_link_list):
                category_link = category_link_list[0]
                category_text = category_link.text_content()
                if category_text in self.category_mapping:
                    category_text = unicode(category_text)
                    category = Category.objects.get(name=self.category_mapping[category_text])
                    print 'Collecting Products for category: ' + category_text
                    link_el = el.xpath('./a')[0]
                    link = link_el.get('href')
                    # link = 'http://localhost/yk/products/'
                    if link:
                        self.collect_products(link, category)
                else:
                    sub_categories_el = el.xpath('./ul')
                    if sub_categories_el:
                        if not len(sub_categories_el[0].xpath('./li[@class="category-vendor-head box-heading"]')):
                            self.parse_category_tree(el.xpath('./ul/li'))

    def collect_products(self, link, category):
        products_page = html.parse(link)
        grid = products_page.xpath('//div[@class="product-list"]')[0]
        products = grid.xpath('./div')
        for product in products:
            url = product.xpath('.//a[1]')[0].get('href')
            # url = 'http://localhost/yk/product1/'
            self.write_product(url, category)
        next_els = products_page.xpath('//div[@class="pagination"]//a[text()=">"]')
        if len(next_els):
            next_el = next_els[0]
            self.collect_products(next_el.get('href'), category)

    def write_product(self, url, category):
        page = html.parse(url)
        name = unicode(page.xpath('.//div[@class="product_title"]/h1')[0].text_content())
        print 'Writing product : ' + name

        try:
            product = Product.objects.get(categories=category, name=name)
        except Product.DoesNotExist:
            product = Product(name=name)
            product.save()
        product.categories.add(category)
        product.save()
        try:
            product_info = ProductInfo.objects.get(product=product, store=self.store)
        except ProductInfo.DoesNotExist:
            product_info = ProductInfo(product=product, store=self.store)
        # TODO: write only if images are new
        # delete existing images first
        images = product.images.all()
        # product.images.clear()
        for image in images:
            image.delete()

        primary_image_url = page.xpath('//div[@class="product-info"]//div[@class="image"]/a')[0].get('href')
        image = Image(image_url=primary_image_url)
        image.save()
        product.images.add(image)
        additional_image_links = page.xpath('//div[@class="image-additional"]/a')
        for image in additional_image_links:
            image_url = image.get('href')
            image = Image(image_url=image_url)
            image.save()
            product.images.add(image)

        price_els = page.xpath('.//div[@class="product-info"]//div[@class="price"]')
        if len(price_els):
            price_el = price_els[0]
        else:
            return
        old_price_els = price_el.xpath('./span[@class="price-old"]')
        if len(old_price_els):
            old_price_el = old_price_els[0]
            old_price_content = old_price_el.text_content()
            old_price = float(re.search('Rs\.([\d,\.]+)', old_price_content).group(1).replace(',', ''))
            product_info.original_price = old_price
            new_price_els = price_el.xpath('./span[@class="price-new"]')
            new_price_el = new_price_els[0]
            new_price_content = new_price_el.text_content()
            new_price = float(re.search('Rs\.([\d,\.]+)', new_price_content).group(1).replace(',', ''))
            product_info.price = new_price
        else:
            price_with_comma = re.search('Price:\s+Rs\.([\d,\.]+)', price_el.text_content()).group(1)
            product_info.price = float(price_with_comma.replace(',', ''))

        product_info.currency = self.currency
        description_text = page.xpath('.//div[@class="product-info"]//div[@class="description"]')[0].text_content()
        product_info.product_code = re.search('Product Code:\s(.+)\\n', description_text).group(1)
        availability_text = re.search('Availability:\s(.+)', description_text).group(1)
        # get vendor
        if availability_text == 'In Stock':
            product_info.availability = 0
        description_el = page.xpath('//div[@id="tab-description"]')[0]
        product.description = tostring(description_el)
        product_info.purchase_url = url
        product.save()
        product_info.save()

        # import bpdb
        #
        # bpdb.set_trace()