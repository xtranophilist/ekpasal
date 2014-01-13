$(document).ready(function () {
    window.vm = new StoreVM(ko_data);
    ko.applyBindings(vm);

});

function StoreVM(data) {
    var self = this;

    self.keyword = ko.observable();
    self.title = ko.observable('Search across e-commerce sites | EkPasal.com');
    self.title.subscribe(set_title);
    self.categories = ko.observableArray();
    self.type = ko.observable();
    self.pages = ko.observable();
    self.page = ko.observable();


    self.fill_generic = function (data) {
        self.type(data['type']);
        self.pages(ko.observable(data['pages']));
        self.page(ko.observable(data['page']));
        if (data.keyword)
            self.keyword(data.keyword);
        self.title(data.title);
    }

    self.fill_generic(data);


    self.fill_category = function (data) {

        if (data.products) {
            self.type('none');
            self.products = ko.observableArray(ko.utils.arrayMap(data.products, function (item) {
                return new ProductVM(item);
            }));

            self.categories(data['source']['categories']);
            self.category = ko.observable(data.source.slug);
            self.fill_generic(data);
            self.title(data.title);
        }
    }

    self.fill_search = function (data) {
        if (data.results) {
            self.type('none');
            self.results = ko.observableArray(ko.utils.arrayMap(data.results, function (item) {
                return new ProductVM(item);
            }));
            self.type('search');

            self.fill_generic(data);
        }
    }


    if (self.type() == 'category') {
        self.fill_category(data);
    }

    if (self.type() == 'product') {
        self.product = ko.observable(new ProductVM(data['product']));
        self.categories = ko.observableArray(data['product']['categories'])
    } else {
        self.product = ko.observable();
    }

    if (self.type() == 'search') {
        self.fill_search(data);

    }

    self.call_search = function (keyword) {
        $.get('/search/' + keyword, function (data) {
            self.fill_search(data);
        });
    }


    var sammy = Sammy(function () {
                this.get('/category/:category_slug', function () {
                    //if the current category is requested don't do anything
                    if (typeof self.category == 'function') {
                        if (self.type() == 'category' && this.params.category_slug == self.category())
                            return;
                        if (this.params.category_slug == self.category()) {
                            self.type('category');
                            return;
                        }
                    }
                    $.get('/category/' + this.params.category_slug, function (data) {
                        self.fill_category(data);
                    });

                });

                this.get('/search/:keyword', function () {
                    if (self.type() == 'search' && this.params.keyword == self.keyword())
                        return;
                    if (this.params.keyword == self.keyword()) {
                        self.type('search');
                        return;
                    }
                    self.call_search(this.params.keyword);

                });

                this.get('/search/*', function () {
//                NOP
                });

                this.notFound = function () {
                    console.log('404 Not Found!')
                }


                this.get('/:product_slug', function () {
                    var slug = this.params.product_slug;
                    if (self.type() == 'product' && slug == self.product().slug)
                        return;
                    if (self.type() == 'search')
                        var products = self['results']
                    else if (self.type() == 'category')
                        var products = self['products']
                    var selected_obj = $.grep(products(), function (i) {
                        return slug == i.slug;
                    })[0];
                    self.product(selected_obj);
                    self.categories(selected_obj.categories);
                    self.type('product');
                    self.title(selected_obj.name)
                });
            }
        )
        ;
    sammy.raise_errors = true;
    sammy.run();

    $('#top-search').on('submit', function (e) {
        sammy.setLocation('/search/' + $('#search-box').val());
        return false;
    })

}

function ProductVM(data) {
    var self = this;
    for (var k in data) {
        self[k] = data[k];
    }

    self.description_text = function () {
        //strip html tags
        var html = self.description;
        var div = document.createElement("div");
        div.innerHTML = html;
        var text = div.textContent || div.innerText || "";
        //strip multiple whitespace with single and return
        return text.replace(/\s+/g, ' ').trim();
    }

    self.get_availability = function () {
        /** @namespace self.availability */
        if (self.availability == 0)
            return 'In Stock';
        else if (self.availability == -1)
            return 'Out of Stock';
        else
            return self.availability
    }

//    self.info = ko.observableArray(ko.utils.arrayMap(data.info, function (item) {
//        return new ProductInfoVM(item);
//    }));

//    self.starting_price = function () {
//        var r = self.info()[0].price;
//        for (var i = 1; i < Object.size(self.info()); i++) {
//            if (self.info()[i].price < r)
//                r = self.info()[i].price;
//        }
//        return r;
//    }

}