var optionBar = $('<div id="option_bar"></div>');

var delButton = $('<img class="side_button" id="del_button" style="width:100%;background:red;" />');
$(delButton).on('click', containers.deleteBox(activeContainer));


var activeContainer = false;

function optionBarAttach(container) {
    getOptionBar().remove();
    activeContainer = $(container)
    
/*    optionBar.css({
            'top': - $(container).css('border-top-width'),
            });*/
    
       
        
    if ($(container).hasClass("empty")) {
        console.log('Empty box options displayed');  
        $(optionBar).append(delButton);
        
        activeContainer.prepend(optionBar);
    } else if ($(container).find('*').hasClass("imgbox")) {
        console.log('Image box options displayed');
        $(optionBar).append(delButton);
         
        activeContainer.prepend(optionBar);
    } else if ($(container).find('*').hasClass("textbox")) {
        console.log('Text box options displayed');
        $(optionBar).append(delButton);
        
        activeContainer.prepend(optionBar);
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
