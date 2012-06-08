/***
 * get live runtime value of an elements css style
 *   http://robertnyman.com/2006/04/24/get-the-rendered-style-of-an-element
 ***/
var getStyle = function (e, styleName) {
    var styleValue = '';
    styleName = styleName.replace(/[A-Z]/g, '-$&').toLowerCase();
    if (document.defaultView && document.defaultView.getComputedStyle) {
        styleValue = document.defaultView.getComputedStyle(e, '').getPropertyValue(styleName);
    }
    else if (e.currentStyle) {
        styleName = styleName.replace(/\-(\w)/g, function (strMatch, p1) {
            return p1.toUpperCase();
        });
        styleValue = e.currentStyle[styleName];
    }
    return styleValue;
}

/***
 * pad(n) - pads input to 'n' places
 ***/
String.prototype.pad = function (n) {
    var str = this;
    while (str.length < n) {
        str = '0' + str;
    }
    return str;
}
