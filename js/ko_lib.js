/**
 * Created by xtranophilist on 1/10/14.
 */

ko.bindingHandlers.flash = {
    init: function (element) {
        $(element).hide().fadeIn('slow');
    }
};

ko.bindingHandlers.fadeIn = {
    init: function(element) {
        $(ko.virtualElements.childNodes(element))
            .filter(function () { return this.nodeType == 1; })
            .hide()
            .fadeIn();
    }
};
ko.virtualElements.allowedBindings.flash = true;