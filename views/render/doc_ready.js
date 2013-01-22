MathJax.Hub.Config({ elements: ["content_area"] });

function handleUpdateTitle(value, settings) {
	jQuery.post('{{=URL("default","call/run/update_title")}}',
		{ page_id:{{=page.id}}, title_content:value },
		function(data){	value = data.title_content; console.log("title update : "); console.log(data); },
		"json");
	return(value);
}

$(document).ready(function(){
	$('button#printpage').click(function() { printing.print_page(); });

    optionBar = initialiseOptionBar($('body'));

	var new_cont = { 'pid': {{=page.id}}, x1: "", y1: "", x2: "", y2: ""};

	$("#main_page").disableTextSelect();

	$(".empty").each(function(index) { containers.defineIsBlank($(this)); });

	//Double click to edit Press enter to save changes. Press Esc to cancel them.
	$("#title_bar").bind('focusin', function() {
		$("#main_page").enableTextSelect()
	}).bind('focusout', function() {
		$("#main_page").disableTextSelect()
	}).editable(handleUpdateTitle, {
		tooltip : "DoubleClick to edit...",
		event : "dblclick"
	});

	$("button#mknewbox").click(function(){
		if (!$(this).hasClass("selected")) {
			$(".selected").removeClass("selected");
			$(this).addClass("selected");
			containers.unsetContainersMobile();
		} else {
			containers.setContainersMobile();
			$(".selected").removeClass("selected");
		}
	});

	$("#content_area").click( function(event){
		optionBarHide();
		saveEditor();
		hideEditor();
	}).mousedown(function(e){
		if ($("button#mknewbox").hasClass("selected")) {
			new_cont['x1'] = (e.pageX - $("div.content_area").offset().left);
			new_cont['y1'] = (e.pageY - $("div.content_area").offset().top);
			if (!(new_cont['x1'] > 0 && new_cont['y1'] > 0 && new_cont['x1'] < $("div.content_area").width() && new_cont['y1'] < $("div.content_area").height()))  {
				new_cont['x1'] = -1;
				new_cont['y1'] = -1;
			}
		}
	}).mouseup(function(e){
		if ($("button#mknewbox").hasClass("selected")) {
			new_cont['x2'] = (e.pageX - $("div.content_area").offset().left);
			new_cont['y2'] = (e.pageY - $("div.content_area").offset().top);
			if (!(new_cont['x2'] > 0 && new_cont['y2'] > 0 && new_cont['x2'] < $("div.content_area").width() && new_cont['y2'] < $("div.content_area").height())) {
				new_cont['x2'] = -1;
				new_cont['y2'] = -1;
			}
			if (new_cont['x1'] > 0 && new_cont['x2'] > 0 && new_cont['y1'] > 0 && new_cont['y2'] > 0) {
				containers.handleCreateContainer(new_cont);
				$(".selected").removeClass("selected");
				containers.setContainersMobile();
				new_cont['x1'] = -1;
				new_cont['y1'] = -1;
				new_cont['x2'] = -1;
				new_cont['y2'] = -1;
			}
		}
	});

	$(".cbox").each(function(index) {
			// WARNING - in future, when we have multiple pages on screen, setting this static here will no longer work.
			$(this).on('dragenter', function(event) { content.handleDragEnter(event, {{=page.id}}); });
			//$(this).on('drop', function(event) { content.handleDrop(event); });
		containers.defineContainerMobile($(this));
		containers.enableOptionBar($(this));
	});

	$(".imgbox").on("dblclick", function(event) {
		containers.toggleMoveResize(this);
	});

	//newly created divs have cross box underneither somhow???
	$('#content_area').append(content.dropCrossBox.crossDiv);
	initialiseEditor();
});