var optionBar = $('<div id="option_bar"></div>');

function optionBarAttach(container) {
    getOptionBar().remove();
    
/*    optionBar.css({
            'top': - $(container).css('border-top-width'),
            });*/
    
    if ($(container).hasClass("empty")) {
        console.log('Empty box options displayed');
        
        $(container).prepend(optionBar);
    } else if ($(container).children().hasClass("imgbox")) {
        console.log('Image box options displayed');
        
        $(container).prepend(optionBar);
    } else if ($(container).children().hasClass("textbox")) {
        console.log('Text box options displayed');
        
        $(container).prepend(optionBar);
    } else {
        console.log('unknown type, no options to display');
        console.log(container);
    }

}

   
function optionBarHide() {
    optionBar.fadeOut(1000);
}

function optionBarShow() {
    optionBar.fadeIn(1000);
}

function getOptionBar() { return optionBar; }
