$(document).ready(function () {
    vm = new StoreVM(ko_data);
    ko.applyBindings(vm);
});

function StoreVM(data) {
    var self = this;

    if (data.products) {
        self.products = ko.observableArray(ko.utils.arrayMap(data.products, function (item) {
            return new ProductVM(item);
        }));
    }

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
        return text.replace(/\s+/g, ' ');
    }

    self.starting_price = function () {
        var r = self.info[0].price;
        for (var i = 1; i < Object.size(self.info); i++) {
            if (self.info[i].price < r)
                r = self.info[i].price;
        }
        return r;
    }
}