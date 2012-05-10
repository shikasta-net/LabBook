// http://www.w3lessons.com/2011/09/disable-enable-deselect-text-selection.html
// Begin:
// Jquery Function to Disable Text Selection
(function($){if($.browser.mozilla){$.fn.disableTextSelect=function(){return this.each(function(){$(this).css({"MozUserSelect":"none"})})};$.fn.enableTextSelect=function(){return this.each(function(){$(this).css({"MozUserSelect":""})})}}else{if($.browser.msie){$.fn.disableTextSelect=function(){return this.each(function(){$(this).bind("selectstart.disableTextSelect",function(){return false})})};$.fn.enableTextSelect=function(){return this.each(function(){$(this).unbind("selectstart.disableTextSelect")})}}else{$.fn.disableTextSelect=function(){return this.each(function(){$(this).bind("mousedown.disableTextSelect",function(){return false})})};$.fn.enableTextSelect=function(){return this.each(function(){$(this).unbind("mousedown.disableTextSelect")})}}}})(jQuery)
// EO Jquery Function
// Usage
// Load Jquery min .js ignore if already done so
// $("element to disable text").disableTextSelect();
// $("element to Enable text").enableTextSelect();
//
