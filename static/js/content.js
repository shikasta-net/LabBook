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
	var box_id = content.dropCrossBox.elementOver.id.substr(1);
	var contentFile = event.dataTransfer.files[0];
	content.handleSaveContent(page_id, box_id, contentFile);
	$(content.dropCrossBox.crossDiv).removeClass('empty');
	$(content.dropCrossBox.elementOver).off('dblclick.empty');
}

content.handleSaveContent = function(page_id, box_id, file_content) {
	var fd = new FormData();
	fd.append("page_id", page_id);
	fd.append("box_id", box_id);
	fd.append("contentFile", file_content);
	fd.append("contentFileName", file_content.name);
	fd.append("contentFileType", file_content.type);
	fd.append("contentFileSize", file_content.size);
	$.ajax({
		url: content.serviceURL + "/upload_content",
		data: fd,
		cache: false,
		contentType: false,
		processData: false,
		type: 'POST',
		dataType: "json",
		success: function(data){
			//console.log("Content upload : ");
			//console.log(data);
			/*
			if (data.error == undefined) {
				$('#c'+data['box_id']).html(data['content']); //This turns out to replace too much and kills the resize divs
			} else {
				alert("There was an error uploading content.");
			}
			*/
		}
	});

}
