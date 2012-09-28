var containers = containers||{};

containers.serviceURL = '/LabBook/containers/call/run';

containers.handleMoveContainer = function (event, ui) {
	var page_width = $('#content_area').width();
	var page_height = $('#content_area').height();
	jQuery.post(containers.serviceURL + '/move_box', { id:$(ui.helper).attr("id"), x:$(ui.position).attr("left")*100/page_width, y:$(ui.position).attr("top")*100/page_height }, function(data){ console.log("move container : ");console.log(data); }, "json");
}

containers.handleResizeContainer = function(event, ui) {
	var page_width = $('#content_area').width();
	var page_height = $('#content_area').height();
	jQuery.post(containers.serviceURL + '/resize_box', { id:$(ui.helper).attr("id"), w:$(ui.size).attr("width")*100/page_width, h:$(ui.size).attr("height")*100/page_height }, function(data){ console.log("resize container : ");console.log(data); }, "json");
}

containers.handleCreateContainer = function(new_cont) {
	var page_width = $('#content_area').width();
	var page_height = $('#content_area').height();
	var dims = { x: Math.min(new_cont['x1'],new_cont['x2'])*100/page_width, y: Math.min(new_cont['y1'],new_cont['y2'])*100/page_height, w: Math.abs(new_cont['x2']-new_cont['x1'])*100/page_width, h: Math.abs(new_cont['y2']-new_cont['y1'])*100/page_height };
	console.log(dims)
	jQuery.post(containers.serviceURL+'/new_box', { page_id:new_cont['pid'], x:dims['x'], y:dims['y'], w:dims['w'], h:dims['h'] }, function(data){
		$("#content_area").append( "<div class='cbox empty' id='box"+data.new_id+"'></div>" );
		$("div#box" + data.new_id).css({
			'top':dims['y']+'%',
			'left':dims['x']+'%',
			'width':dims['w']+'%',
			'height':dims['h']+'%'
		});
		$("div#box" + data.new_id).on('dragenter', content.handleDragEnter);
		$("div#box" + data.new_id).on('drop', content.handleDrop);
		containers.defineContainerMobile($("div#box" + data.new_id));
		containers.defineIsBlank($("div#box" + data.new_id));
		containers.enableOptionBar($("div#box" + data.new_id));
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
	});
}

containers.unsetContainersMobile = function(target) {
	if(typeof target == 'undefined') target = $("div.cbox");
	target.each(function (index) { $(this).draggable("option", "disabled", true).resizable("option", "disabled", true); });
}
containers.setContainersMobile = function(target) {
	if(typeof target == 'undefined') target = $("div.cbox");
	target.each(function (index) { $(this).draggable("option", "disabled", false).resizable("option", "disabled", false); });
}


containers.enableOptionBar = function(target) {
	target.on('click', function(event) {
		event.stopPropagation();
		optionBarShow($(this));
	});
}

containers.dissableOptionBar = function(target) {
	target.off('click');
}


containers.defineIsBlank = function(target) {
	target.addClass('empty');
/*	target.on('dblclick.empty', function(event) {
		$(event.target).prepend("<div class='textbox' id='"+$(event.target).attr('id').replace('c','txt')+"'><p></p></div>"); //the p is needed to force mce to be the size of the container, sadly it removes it if you dont put anything in it first time
		target.removeClass("empty");
		target.unbind('dblclick');
		containers.defineIsEditable($('#'+$(event.target).attr('id')));
		event.stopImmediatePropagation();
		showEditor(target)
	})*/
}
/*
containers.defineIsEditable = function(target) {
	target.bind('dblclick', function(event) {
		event.stopPropagation();
		optionBarHide();
		containers.handleDynamicTextEditor($(event.target));
	});
}
*/

containers.handleDynamicTextEditor = function(target){
	if(target.hasClass('cbox')) {
		var targetCBox = target;
		var targetTBox = target.children('div.textbox');
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
	targetCBox.unbind('dblclick'); //protect the double clicking when the editor is open already
	containers.dissableOptionBar(targetCBox);
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
	jQuery.post(containers.serviceURL+'/del_box', { box_id:target.attr("id") }, function(data){ console.log("remove container : ");console.log(data); }, "json");
	target.detach();
	containers.setContainersMobile();
	$(".selected").removeClass("selected");
}

containers.clearContent = function (target) {
	$.ajax({
		url: '/LabBook/content/call/run/delete',
		data: { box_id: activeContainer.attr("id") },
		type: 'GET',
		error: function(data) { console.log('Error on AJAX delete content request'); },
		success: function(data) {
			if (activeContainer.children(".clipbox").length != 0) {
				childBox = activeContainer.children(".clipbox").first();
				$.ajax({
					url: '/LabBook/content/call/run/delete',
					data: { box_id: activeContainer.attr("id") },
					type: 'GET',
					error: function(data) { console.log('Error on AJAX delete content request'); }
				});
			}
		}
	});
	activeContainer.children("*").not('ui-resizable-handle').detach()
	activeContainer.attr("type", "");
}
