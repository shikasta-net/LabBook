var textEd = false;


function initialiseEditor() { 
    textEd = new tinyMCE.Editor('textEditor', {
            mode : "none",
            theme : "simple",
            skin: "default"
    //       content_css : "{{=URL('/static/css','tinyMCE_custom.css')}}"
    });     
    textEd.render();
    textEd.hide();
}


function showEditor(target) {
    textEd.show();
    textEd.setContent(target.children(".textbox").html());
}

function hideEditor() {
    textEd.hide();
}
