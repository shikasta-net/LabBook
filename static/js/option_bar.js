optionBar = null;

function initialiseOptionBar(body_element) {
    var optionBarInit = $(
                      ['<div id="option_bar">',
                       '<img class="side_button" id="del_button" title="Delete this container" style="width:100%;background:red;" />',
                       '<img class="side_button" id="text_button" title="Edit the text of this container" style="width:100%;background:blue;" />',
                       '<img class="side_button" id="clear_content_button" title="Clear the content of this container" style="width: 100%; background:    goldenrod;" />',
                       '<img class="side_button" id="test_button" title="Example button does nothing... much" style="width:100%;background:grey;" />',
                       '<img class="side_button" id="wrap_button" title="Rescale/move box content" style="width:100%;background:purple;" />',
                       '<img class="side_button" id="unwrap_button" title="Scale content to box" style="width:100%;background:cyan;" />',
                       '<img class="side_button" id="set_pdf_page" title="Set PDF page" style="width:100%;background:yellow" />'].join('')
                      );
    optionBar = optionBarInit;
    body_element.append(optionBar);
    optionBarHide();
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
    
    $('#wrap_button').on('click', function(event) {
                         event.stopImmediatePropagation();
                         console.log('Wrapping ' + activeContainer.attr('id'));
                         $.ajax({
                                url: containers.serviceURL + "/wrap_box",
                                data: { box_id: activeContainer.attr('id') },
                                cache: false,
                                dataType: 'json',
                                type: 'POST',
                                success: function(data){
                                $.ajax({
                                       url: "/LabBook/render/box/" + data['new_id'],
                                       type: 'GET',
                                       success: function(data) {
                                            // Refresh dynamic css
                                            // This method leads to unacceptable flickering. In future, we will have to look into
                                            // including box css directly on the page (ie in style tags, rather than a link tag)
                                            // as this will allow the CSS to be loaded synchronously before replacing the box element
                                            // rather than asynchronously by modifying the link href (which causes the flicker)
                                            $('#dynamic_css').each(function() {
                                                                   this.href = this.href.replace(/refresh=.*|$/, '&refresh=' + new Date().getTime());
                                                                   });
                                            var newParent = $(data);
                                            activeContainer.replaceWith(newParent);
                                            newParent.on('dragenter', content.handleDragEnter);
                                            newParent.on('drop', content.handleDrop);
                                            containers.defineContainerMobile(newParent);
                                            containers.enableOptionBar(newParent);

                                            setOptions();
                                       },
                                       error: function (data) {
                                       console.log('Error wrapping box: ' + data);
                                       }
                                       });
                                }
                                });
                         });
    
    $('#unwrap_button').on('click', function(event) {
                        event.stopImmediatePropagation();
                        console.log('Unwrapping ' + activeContainer.attr('id'));
                        $.ajax({
                               url: containers.serviceURL + '/unwrap_box',
                               data: { box_id: activeContainer.attr('id') },
                               cache: false,
                               type: 'POST',
                               dataType: 'json',
                               success: function(data) {
                               console.log('Unwrap successful (refresh)'+data['child_id']);
                               $.ajax({
                                      url: "/LabBook/render/box/" + data['child_id'],
                                      type: 'GET',
                                      success: function(data) {
                                      // Refresh dynamic css
                                      // See wrap_box for discussion
                                      $('#dynamic_css').each(function() {
                                                             this.href = this.href.replace(/refresh=.*|$/, '&refresh=' + new Date().getTime());
                                                             });
                                      var childBox = $(data);
                                      activeContainer.replaceWith(childBox);
                                      childBox.on('dragenter', content.handleDragEnter);
                                      childBox.on('drop', content.handleDrop);
                                      containers.defineContainerMobile(childBox);
                                      containers.enableOptionBar(childBox);
                                      
                                      setOptions();
                                      },
                                      error: function (data) {
                                      console.log('Error unwrapping box: ' + data);
                                      }
                                      });

                               
                               }
                               });
                        });
    
    $('#set_pdf_page').on('click', function(event) {
                         event.stopImmediatePropagation();
                         console.log('Changing PDF page');
                         var pdf_page = window.prompt("Set the displayed page:", "1");
                         if (pdf_page) {
                         var targetID = activeContainer.attr('id');
                         if (activeContainer.attr('type') == 'box') {
                            targetID = activeContainer.find('.imgbox').first().attr('id');
                         }
                         console.log("Setting PDF page for " + targetID + " to " + pdf_page);
                          $.ajax({
                                 url: content.serviceURL + '/set_content_meta',
                                 data: { box_id: targetID, meta_json: JSON.stringify({ pdf_page: pdf_page }) },
                                 cache: false,
                                 type: 'POST',
                                 dataType: 'json',
                                 success: function(data) {
                                 console.log('Metadata set OK');
                                 }

                                 });
                          }
                          });
                          
    return optionBar;
}

var activeContainer = false;

function attach(target) {
	activeContainer = $(target);
//	optionBar.detach();
//	activeContainer.append(optionBar);
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
        $('#unwrap_button').show();
        
	} else if (activeContainer.attr("type") == "text/html") {
		console.log('Text box options displayed');
		$('#text_button').show();
		/* Option bar makes display equations jump about */
        $('#clear_content_button').show();

	} else {
		console.log('Other type, general options displayed');
        $('#clear_content_button').show();
        $('#wrap_button').show();
        
	}
    
    if (activeContainer.attr("type") == "application/pdf"
        || activeContainer.find('.imgbox').attr("type") == "application/pdf") {
        $("#set_pdf_page").show();
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
