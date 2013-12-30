__author__ = 'xtranophilist'
from lxml import html

# import os
# import sys
#
# parent_dir = os.path.join(os.path.dirname(__file__), '..', '..'),
# sys.path.append(parent_dir)
#
# print parent_dir

from store import models


class Yeskantipur():
    def __init__(self):
        pass

    # root_url = 'http://www.yeskantipur.com'
    root_url = 'http://localhost/yk'

    category_mapping = {
        'Gents': 'Men'
    }

    def mine(self):
        root_page = html.parse(self.root_url)
        root_category_elements = root_page.xpath('//*[@id="column-left"]//ul[@id="navigation"]/li')
        self.parse_category_tree(root_category_elements)

    def parse_category_tree(self, tree):
        for el in tree:
            category_link_list = el.xpath('./a[1]')
            if len(category_link_list):
                category_link = category_link_list[0]
                category_text = category_link.text_content()
                # print category_text
                if category_text in self.category_mapping:
                    self.collect_products(el, category_text)
                else:
                    sub_categories_el = el.xpath('./ul')
                    if sub_categories_el:
                        # import bpdb;
                        #
                        # bpdb.set_trace()
                        if not len(sub_categories_el[0].xpath('./li[@class="category-vendor-head box-heading"]')):
                            self.parse_category_tree(el.xpath('./ul/li'))
                            # pass

                            # import bpdb;bpdb.set_trace()

                            # import bpdb
                            # bpdb.set_trace()


    def collect_products(self, el, category_text):
        link_el = el.xpath('./a')[0]
        link = link_el.get('href')
        link = 'http://localhost/yk/products/'
        if link:
            products_page = html.parse(link)
            grid = products_page.xpath('//div[@class="product-grid"]')[0]
            products = grid.xpath('./div')
            for product in products:
                url = product.xpath('.//a[1]')[0].get('href')
                url = 'http://localhost/yk/product/'
                self.write_product(url, category_text)

    def write_product(self, url, category_text):
        page = html.parse(url)
        import bpdb;

        bpdb.set_trace()
        title = page.xpath('.//div[@class="product_title"]/h1')[0].text_content()
