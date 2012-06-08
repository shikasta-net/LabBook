var textEd = false;
var currentTarget = false;


function initialiseEditor() { 
    $('body').append("<div id='textEditorContainer'><div id='textEditor'></div></div>");  
    textEd = new tinyMCE.Editor('textEditor', {
            mode : "none",
            theme : "simple",
            skin: "default",
    //       content_css : "{{=URL('/static/css','tinyMCE_custom.css')}}",
            setup: function(ed) {
                ed.onKeyUp.add(function(ed, e) {
                    currentTarget.children('.textbox').html(ed.getContent());
                });
            }
    });     
    textEd.render();
    hideEditor();
}


function showEditor(target) {
    currentTarget = target;
    textEd.setContent('<p></p>');
    $('#textEditorContainer').slideDown('1000');
//    textEd.setContent(target.children(".textbox").html());
    textEd.setProgressState(1);
    jQuery.post(serviceURL + '/get_content', { box_id:currentTarget.attr("id").replace('c','') }, function(data){ textEd.setContent(data); }, "html");
    textEd.setProgressState(0);
    textEd.focus();
}

function hideEditor() {
    currentTarget = false;
    $('#textEditorContainer').slideUp('1000');
}

function saveEditor() {
    textEd.setProgressState(1);
    if (window.BlobBuilder) {
        var bb = new BlobBuilder();
    } else if (window.MozBlobBuilder) {
        var bb = new MozBlobBuilder();
    } else if (window.MSBlobBuilder) {
        var bb = new MSBlobBuilder();
    } else if (window.WebKitBlobBuilder) {
        var bb = new WebKitBlobBuilder();
    } else {
        throw "No BlobBuilder implementation";
    }
    bb.append(textEd.getContent());
    var blob = bb.getBlob('text/html');
    content.handleSaveContent(pageID, currentTarget.attr("id").replace('c',''), blob, { name:'textbox'+currentTarget.attr("id").replace('c','')+'.html', type:'text/html', size: blob.size });
    textEd.setProgressState(0);
}
