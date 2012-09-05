
function initialiseOptionBar(body_element) {
    var optionBar = $(
    ['<div id="option_bar">',
    '<img class="side_button" id="del_button" title="Delete this container" style="width:100%;background:red;" />',
    '<img class="side_button" id="text_button" title="Edit the text of this container" style="width:100%;background:blue;" />',
    '<img class="side_button" id="clear_content_button" title="Clear the content of this container" style="width: 100%; background:    goldenrod;" />',
    '<img class="side_button" id="test_button" title="Example button does nothing... much" style="width:100%;background:grey;" />'].join('')
    );
    body_element.append(optionBar);
    $('#del_button').on('click', function(event) { 
      event.stopImmediatePropagation(); 
      if (activeContainer.attr('type') != '') {
          containers.clearContent(activeContainer);
      }
      containers.deleteBox(activeContainer); 
      });
      
      $('#text_button').on('click', function(event) {
      event.stopImmediatePropagation();
      if (activeContainer.children('.textbox').length == 0) {
          activeContainer.append('<div class="textbox"></div>');
      }
      showEditor(activeContainer);
      });
      
      $('#clear_content_button').on('click', function(event) {
      event.stopImmediatePropagation();
      containers.clearContent(activeContainer);
      setOptions();
      });
      
      $('#test_button').on('click', function(event) { console.log('test button'); event.stopImmediatePropagation(); });

    return optionBar;
}

var activeContainer = false;

function attach(target) {
	activeContainer = $(target);
	optionBar.detach();
	activeContainer.append(optionBar);
    setOptions();
    
    $(optionBar).position({
        my: "left top",
        at: "right top",
        of: activeContainer,
        collision: 'fit'
    });
}

/*	optionBar.css({
			'top': - activeContainer.css('border-top-width'),
			});*/
			
function setOptions() {

    $(optionBar).children().hide();
    
	if (activeContainer.attr("type") == ("")) {
		console.log('Empty box options displayed');
		$('#del_button').show();
		$('#text_button').show();
		$('#test_button').show();

	} else if (activeContainer.attr("type") == "box") {
		console.log('Childbox box options displayed');
        $('#clear_content_button').show();
        
	} else if (activeContainer.attr("type") == "text/html") {
		console.log('Text box options displayed');
		$('#text_button').show();
		/* Option bar makes display equations jump about */
        $('#clear_content_button').show();

	} else {
		console.log('Other type, general options displayed');
        $('#clear_content_button').show();
        
	}

}


function optionBarHide() {
    optionBar.fadeOut(100);
//	optionBar.children().detach();
//	optionBar.remove();
}

function optionBarShow(target) {
    optionBar.fadeIn(100);
//	optionBar.children().detach();
//	optionBar.remove();
 	attach(target);
}

function getOptionBar() { return optionBar; }
