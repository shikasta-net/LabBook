var containers = containers||{};

containers.handleMoveContainer = function (event, ui) {
    jQuery.post(serviceURL + '/move_box', { id:$(ui.helper).attr("id"), x:$(ui.position).attr("left")/pxPerem, y:$(ui.position).attr("top")/pxPerem }, function(data){ console.log("move container : ");console.log(data); }, "json");
}

containers.handleResizeContainer = function(event, ui) {
    jQuery.post(serviceURL + '/resize_box', { id:$(ui.helper).attr("id"), w:$(ui.size).attr("width")/pxPerem, h:$(ui.size).attr("height")/pxPerem }, function(data){ console.log("resize container : ");console.log(data); }, "json");
}

containers.handleCreateContainer = function(new_cont) {
    var dims = { x: Math.min(new_cont['x1'],new_cont['x2']), y: Math.min(new_cont['y1'],new_cont['y2']), w: Math.abs(new_cont['x2']-new_cont['x1']), h: Math.abs(new_cont['y2']-new_cont['y1']) };
    jQuery.post(serviceURL+'/new_box', { page_id:new_cont['pid'], x:dims['x']/pxPerem, y:dims['y']/pxPerem, w:dims['w']/pxPerem, h:dims['h']/pxPerem }, function(data){  
        $("#content_area").append( "<div class='cbox empty' id='c"+data.new_id+"'></div>" );   
        $("div#c" + data.new_id).css({ 
            'top':dims['y']+'px',
            'left':dims['x']+'px',
            'width':dims['w']+'px',
            'height':dims['h']+'px'
        });
        $("div#c" + data.new_id).on('dragenter', content.handleDragEnter);
        $("div#c" + data.new_id).on('drop', content.handleDrop);
        containers.defineContainerMobile($("div#c" + data.new_id));   
        containers.defineIsBlank($("div#c" + data.new_id));
        console.log("create container : ");console.log(data);             
    }, "json"); 
}

containers.defineContainerMobile = function(target) {
    target.draggable({    
        snap: ".cbox",
        snapTolerance: 5,
        snapMode: "outer",
        containment: "parent",
        stop: function(event, ui) { containers.handleMoveContainer(event, ui); }
    }).resizable({ 
        containment: "parent",       
        stop: function(event, ui) { containers.handleResizeContainer(event, ui); }
    }).click( function(event) {
        event.stopImmediatePropagation();        
        optionBarAttach(this);        
    }); 
}

containers.unsetContainersMobile = function(target) {
    if(typeof target == 'undefined') target = $("div.cbox");  
    target.each(function (index) { $(this).draggable("option", "disabled", true).resizable("option", "disabled", true); });
}
containers.setContainersMobile = function(target) {
    if(typeof target == 'undefined') target = $("div.cbox");
    target.draggable("option", "disabled", false).resizable("option", "disabled", false);
}

containers.defineIsBlank = function(target) {
    target.addClass('empty');
    target.on('dblclick.empty', function(event) {   
        $(event.target).prepend("<div class='textbox' id='"+$(event.target).attr('id').replace('c','txt')+"'><p></p></div>"); //the p is needed to force mce to be the size of the container, sadly it removes it if you dont put anything in it first time
        target.removeClass("empty");
        target.unbind('dblclick');   
        containers.defineIsEditable($('#'+$(event.target).attr('id')));
        containers.handleDynamicTextEditor($('#'+$(event.target).attr('id')));
    })
}

containers.defineIsEditable = function(target) {
    target.bind('dblclick', function(event) {
        event.stopPropagation();  
        containers.handleDynamicTextEditor($(event.target));
    });
}

containers.handleDynamicTextEditor = function(target){
    if(target.hasClass('cbox')) {
        var targetCBox = target;
        var targetTBox = target.child('div.textbox');
    } else if(target.hasClass('textbox')) {
        var targetCBox = target.parent('div.cbox');
        var targetTBox = target;
    } else {
        var targetCBox = target.parents('div.cbox');
        var targetTBox = target.parents('div.textbox');
    }
    if (!targetCBox || !targetTBox) {
        throw "handleDynamicTextEditor called on something which isn't a child of a cbox or a textbox: " + $(target)[0].tagName
    }
    containers.unsetContainersMobile(targetCBox);
    var id = $(targetTBox).attr('id');
    if(tinyMCE.getInstanceById(id)) {        
        tinyMCE.getInstanceById(id).show();
        tinyMCE.execCommand('mceFocus', false, id);
    } else {
        tinyMCE.execCommand('mceAddControl', false, id);           
    }
}

containers.toggleMoveResize = function(toggleElement) {
    if ($(toggleElement).hasClass('ui-draggable')) { 
        $(toggleElement).css('border', 'none');
        $(toggleElement).draggable('destroy');
        $(toggleElement).resizable('destroy');
    } else {
        $(toggleElement).css('border', '1px dotted red');
        $(toggleElement).draggable({stop: function(event, ui) { containers.handleMoveContainer(event, ui); }});
        $(toggleElement).resizable({stop: function(event, ui) { containers.handleResizeContainer(event, ui); }});
    }
}

containers.deleteBox =  function(target) {    
    jQuery.post(serviceURL+'/del_box', { box_id:target.attr("id").replace('c','') }, function(data){ console.log("remove container : ");console.log(data); }, "json");
    target.detach();
    containers.setContainersMobile();
    $(".selected").removeClass("selected");
}
