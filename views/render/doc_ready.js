MathJax.Hub.Config({ elements: ["content_area"] });

//~ function handleUpdateTitle(value, settings) {
	//~ console.log(settings.submitdata);
	//~ jQuery.post('{{=URL("default","call/run/update_title")}}',
		//~ { page_id:settings.submitdata['page_id'], title_content:value },
		//~ function(data){	value = data.title_content; console.log("title update : "); console.log(data); },
		//~ "json");
	//~ return(value);
//~ }

function pageID(target) {
	return target.parents("div.page").attr('id').replace('page','');
}


function initialise_pages() {
	$('button#printpage').click(function() { printing.print_page(); });

	optionBar = initialiseOptionBar($('body'));

	var new_cont = { 'pid': "", x1: "", y1: "", x2: "", y2: ""};

	$(".empty").each(function(index) { containers.defineIsBlank($(this)); });

	$(".pages").disableTextSelect();

	//Double click to edit Press enter to save changes. Press Esc to cancel them.
	$(".title_bar").bind('focusin', function() {
		$(".page").enableTextSelect()
	}).bind('focusout', function() {
		$(".page").disableTextSelect()
	}).editable('{{=URL("default","call/run/update_title")}}', {
		tooltip : "DoubleClick to edit...",
		event : "dblclick",
		name : 'title_content',
		id : 'page_id'
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

	$(".content_area").click( function(event){
		optionBarHide();
		saveEditor();
		hideEditor();
	}).mousedown(function(e){
		if ($("button#mknewbox").hasClass("selected")) {
			new_cont['x1'] = (e.pageX - $(e.target).offset().left);
			new_cont['y1'] = (e.pageY - $(e.target).offset().top);
			if (!(new_cont['x1'] > 0 && new_cont['y1'] > 0 && new_cont['x1'] < $(e.target).width() && new_cont['y1'] < $(e.target).height()))  {
				new_cont['x1'] = -1;
				new_cont['y1'] = -1;
			}
		}
	}).mouseup(function(e){
		if ($("button#mknewbox").hasClass("selected")) {
			new_cont['x2'] = (e.pageX - $(e.target).offset().left);
			new_cont['y2'] = (e.pageY - $(e.target).offset().top);
			if (!(new_cont['x2'] > 0 && new_cont['y2'] > 0 && new_cont['x2'] < $(e.target).width() && new_cont['y2'] < $(e.target).height())) {
				new_cont['x2'] = -1;
				new_cont['y2'] = -1;
			}
			if (new_cont['x1'] > 0 && new_cont['x2'] > 0 && new_cont['y1'] > 0 && new_cont['y2'] > 0) {
				new_cont['pid'] = pageID($(e.target));
				containers.handleCreateContainer($(e.target), new_cont);
				$(".selected").removeClass("selected");
				containers.setContainersMobile();
				new_cont['pid'] = "";
				new_cont['x1'] = -1;
				new_cont['y1'] = -1;
				new_cont['x2'] = -1;
				new_cont['y2'] = -1;
			}
		}
	});

	$(".cbox").each(function(index) {
			// WARNING - in future, when we have multiple pages on screen, setting this static here will no longer work.
			$(this).on('dragenter', function(event) { content.handleDragEnter(event, pageID($(this))); });
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
}