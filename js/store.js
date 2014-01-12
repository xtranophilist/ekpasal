$(document).ready(function () {
    vm = new StoreVM(ko_data);
    ko.applyBindings(vm);
});

function CategoryVM(data){
    var self = this;
    for (var k in data) {
        self[k] = ko.observable(data[k]);
    }
}

function StoreVM(data) {
    var self = this;
    self.type = ko.observable(data['type']);
    self.title = ko.observable('Search across e-commerce sites | EkPasal.com');
    self.title.subscribe(set_title);
    self.categories = ko.observableArray();

    self.fill_category = function (data) {

        if (data.products) {
            self.type('none');
            self.products = ko.observableArray(ko.utils.arrayMap(data.products, function (item) {
                return new ProductVM(item);
            }));

            self.categories(ko.utils.arrayMap(data['source']['categories'], function (item) {
                return new CategoryVM(item);
            }));
            self.category = ko.observable(data.source.slug);
            self.type('category');
            self.title(data.title);
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


    var sammy = Sammy(function () {
        this.get('/category/:category_slug', function () {
            //if the current category is requested don't do anything
            if (typeof self.category == 'function') {
                if (self.type == 'category' && this.params.category_slug == self.category())
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
        this.get('/:product_slug', function () {
            var slug = this.params.product_slug;
            if (self.type() == 'product' && slug == self.product().slug)
                return;
            var selected_obj = $.grep(self.products(), function (i) {
                return slug == i.slug;
            })[0];
            self.product(selected_obj);
            self.type('product');
            self.title(selected_obj.name)
        });
    });
    sammy.raise_errors = true;
    sammy.run();

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

    self.info = ko.observableArray(ko.utils.arrayMap(data.info, function (item) {
        return new ProductInfoVM(item);
    }));

    self.starting_price = function () {
        var r = self.info()[0].price;
        for (var i = 1; i < Object.size(self.info()); i++) {
            if (self.info()[i].price < r)
                r = self.info()[i].price;
        }
        return r;
    }

}

function ProductInfoVM(data) {
    var self = this;
    for (var k in data) {
        self[k] = data[k];
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
}