var content = content||{};

content.dropCrossBox = new crossBox();

content.serviceURL = '/LabBook/content/call/run';

content.handleDragEnter = function(event, page_id) {
	event.stopPropagation();
	event.preventDefault();
	content.dropCrossBox.elementOver = event.target;
	content.dropCrossBox.pageOver = page_id;
	content.dropCrossBox.resizeAndPosition(event.target.id);
	content.dropCrossBox.show()
}

content.handleDrop = function(event) {
	event.stopPropagation();
	event.preventDefault();
	var page_id = content.dropCrossBox.pageOver;
	var box_id = content.dropCrossBox.elementOver.id;
	var contentFile = event.dataTransfer.files[0];
	content.handleSaveContent(page_id, box_id, contentFile);
	$(content.dropCrossBox.elementOver).removeClass('empty');
	$(content.dropCrossBox.elementOver).off('dblclick.empty');
}

content.handleSaveContent = function(page_id, box_id, file_content, metadata) {
	var fd = new FormData();
	fd.append("page_id", page_id);
	fd.append("box_id", box_id);
	fd.append("contentFile", file_content);
	fd.append("contentFileName", metadata.name);
	fd.append("contentFileType", metadata.type);
	fd.append("contentFileSize", metadata.size);
	$.ajax({
		url: this.serviceURL + "/upload",
		data: fd,
		cache: false,
		contentType: false,
		processData: false,
		type: 'POST',
		success: function(data){
		    var dom_box = $('#' + data);
            $.ajax({
                url: "/LabBook/render/box_content/" + data,
                data: { box_id: data },
                type: 'GET',
                success: function(data) {
                    dom_box.html(data);
                    MathJax.Hub.Queue(["Typeset", MathJax.Hub, dom_box.children(".textbox").get(0)]);
                }
            });
		}
	});

}
