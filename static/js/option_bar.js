var optionBar = $('<div id="option_bar"></div>');

var delButton = $('<img class="side_button" id="del_button" style="width:100%;background:red;" />');
$(delButton).on('click', function(event) { event.stopImmediatePropagation(); containers.deleteBox(activeContainer); });

var testButton = $('<img class="side_button" id="test_button" style="width:100%;background:blue;" />');
$(testButton).on('click', function(event) { event.stopImmediatePropagation(); showEditor(activeContainer) });

var activeContainer = false;

function attach(target) {
    activeContainer = $(target)

/*    optionBar.css({
            'top': - activeContainer.css('border-top-width'),
            });*/



    if (activeContainer.hasClass("empty")) {
        console.log('Empty box options displayed');
        $(optionBar).append(delButton);

        activeContainer.prepend(optionBar);
    } else if (activeContainer.find('*').hasClass("imgbox")) {
        console.log('Image box options displayed');
        $(optionBar).append(delButton);

        activeContainer.prepend(optionBar);
    } else if (activeContainer.find('*').hasClass("textbox")) {
        console.log('Text box options displayed');
        $(optionBar).append(delButton);
        $(optionBar).append(testButton);

        activeContainer.prepend(optionBar);
    } else {
        console.log('unknown type, no options to display');
        console.log(activeContainer);
    }

}


function optionBarHide() {
    optionBar.empty();
    optionBar.remove();
}

function optionBarShow(target) {
    optionBar.empty();
    optionBar.remove();
    attach(target);
}

function getOptionBar() { return optionBar; }
