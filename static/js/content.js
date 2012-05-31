var content = content||{};

content.dropCrossBox = new crossBox();

content.handleDragEnter = function(event) {
    event.stopPropagation();
    event.preventDefault();
    content.dropCrossBox.elementOver = $(this);
    content.dropCrossBox.resizeAndPosition(this.id);
    content.dropCrossBox.show()
}

content.handleDrop = function(event) {
    console.log('boom');
    event.originalEvent.stopPropagation();
    event.originalEvent.preventDefault();
    var box_id = content.dropCrossBox.elementOver.id.substr(1);
    var contentFile = event.dataTransfer.files[0];    
    content.handleSaveContent(box_id, contentFile, contentFile);
    $(content.dropCrossBox.crossDiv).removeClass('empty');
    $(content.dropCrossBox.elementOver).off('dblclick.empty');
}

content.handleSaveContent = function(page_id, box_id, content, metadata) {
    var fd = new FormData();    
    fd.append("page_id", page_id);
    fd.append("box_id", box_id);
    fd.append("contentFile", content);
    fd.append("contentFileName", metadata.name);
    fd.append("contentFileType", metadata.type);
    fd.append("contentFileSize", metadata.size);
    $.ajax({
        url: serviceURL+"/upload_content",
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
