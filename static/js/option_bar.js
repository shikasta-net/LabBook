var optionBar = $('<div id="option_bar"></div>');

var delButton = $('<img class="side_button" id="del_button" title="Delete this container" style="width:100%;background:red;" />');
$(delButton).on('click', function(event) { event.stopImmediatePropagation(); containers.deleteBox(activeContainer); });

var editTextButton = $('<img class="side_button" id="text_button" title="Edit the text of this container" style="width:100%;background:blue;" />');
$(editTextButton).on('click', function(event) {
	event.stopImmediatePropagation();
	showEditor(activeContainer);
});



var testButton = $('<img class="side_button" id="test_button" title="Example button does nothing... much" style="width:100%;background:grey;" />');
$(testButton).on('click', function(event) { console.log('test button'); event.stopImmediatePropagation(); });

var activeContainer = false;

function attach(target) {
	activeContainer = $(target)

/*	optionBar.css({
			'top': - activeContainer.css('border-top-width'),
			});*/



	if (activeContainer.hasClass("empty")) {
		console.log('Empty box options displayed');
		$(optionBar).append(delButton);
		$(optionBar).append(editTextButton);
		$(optionBar).append(testButton);

		activeContainer.prepend(optionBar);
	} else if (activeContainer.find('*').hasClass("imgbox")) {
		console.log('Image box options displayed');
		$(optionBar).append(delButton);

		activeContainer.prepend(optionBar);
	} else if (activeContainer.find('*').hasClass("textbox")) {
		console.log('Text box options displayed');
		$(optionBar).append(delButton);
		$(optionBar).append(editTextButton);

		activeContainer.prepend(optionBar);
	} else {
		console.log('unknown type, no options to display');
		console.log(activeContainer);
	}

}


function optionBarHide() {
	optionBar.children().detach();
	optionBar.remove();
}

function optionBarShow(target) {
	optionBar.children().detach();
	optionBar.remove();
	attach(target);
}

function getOptionBar() { return optionBar; }
