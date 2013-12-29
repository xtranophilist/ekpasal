__author__ = 'xtranophilist'
from lxml import html


class Yeskantipur():
    def __init__(self):
        pass

    # root_url = 'http://www.yeskantipur.com'
    root_url = 'http://localhost/yk'

    category_mapping = {
        'Gents': 'Men'
    }

    def parse_category_tree(self, tree):
        for el in self.root_category_elements:
            category_link = el.xpath('./a[1]')[0]
            category_text = category_link.text_content()
            # if category_text in
            import bpdb

            bpdb.set_trace()

            # import bpdb
            # bpdb.set_trace()

    def mine(self):
        root_page = html.parse(self.root_url)
        root_category_elements = root_page.xpath('//*[@id="column-left"]//ul[@id="navigation"]/li')
        self.parse_category_tree(root_category_elements)








