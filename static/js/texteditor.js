var textEd = false;
var edCurrentTarget = false;
var KEYLEFT = 37;
var KEYRIGHT = 39;
var DOLLAR = 36;
var CTRLDOLLAR = 52;

function initialiseEditor() { 
    $('body').append("<div id='textEditorContainer'><div id='textEditor'></div></div>");  
    textEd = new tinyMCE.Editor('textEditor', {
            mode : "none",
            theme : "simple",
            skin: "default",
            content_css : "../../css/page_layout.css",
	    forced_root_block: false,
            setup: function(ed) {
		ed.onNodeChange.add(function(ed, cm, e) {
		});
                ed.onKeyPress.add(function(ed, e) {

			/*if (e.keyCode == KEYLEFT 
				&& ed.selection.isCollapsed() 
				&& ed.selection.getRng(true).startOffset == 0
				&& ed.selection.getRng(true).startContainer.parentElement.nodeName == 'SPAN') {
					e.preventDefault();
					e.stopPropagation();
					console.log('cursor leaving SPAN keypress');
			}*/	
			// If we're currently editing an equation...
			if (ed.dom.hasClass(ed.selection.getNode(), 'eqn')) {
				// Pressed $ in inline eqn? Boost eqn to display
				if (e.charCode == DOLLAR && ed.dom.hasClass(ed.selection.getNode(), 'inline')) {
					e.preventDefault();
					e.stopPropagation();
					ed.dom.removeClass(ed.selection.getNode(), 'inline');
					ed.dom.addClass(ed.selection.getNode(), 'display');
				}
				// Pressed Ctrl-$ in inline? Remove eqn and leave plaintext
				if (e.charCode == CTRLDOLLAR && ed.dom.hasClass(ed.selection.getNode(), 'inline')) {
					e.preventDefault();
					e.stopPropagation();
					var temp = ed.selection.getNode().innerHTML;
					ed.dom.remove(ed.selection.getNode());
					ed.selection.setContent(temp);
				}
				// Pressed Ctrl-$ in display eqn? Reduce to inline eqn
				if (e.charCode == CTRLDOLLAR && ed.dom.hasClass(ed.selection.getNode(), 'display')) {
					e.preventDefault();
					e.stopPropagation();
					ed.dom.removeClass(ed.selection.getNode(), 'display');
					ed.dom.addClass(ed.selection.getNode(), 'inline');
				}

			} else {
				// $ pressed outside equation? Make new eqn.
				if (e.charCode == DOLLAR) {
					e.preventDefault();
					e.stopPropagation();
					var newEqnID = ed.dom.uniqueId('eqn_');
					var newEqn = ed.dom.create('span', {id: newEqnID, class: 'eqn inline'}, 'x');
					ed.selection.setContent(newEqn.outerHTML);
					ed.selection.select(ed.dom.select('#'+newEqnID)[0].firstChild);
				}
			}
	
		});

		// Update content box every time user presses a key.
		// TODO: Less intensive update scheme? (eg track caret position and update only updated elements?) Complicated!
		ed.onKeyUp.add(function(ed, e) {
			
			/*if (e.keyCode == KEYLEFT 
				&& ed.selection.isCollapsed() 
				&& ed.selection.getRng(true).startOffset == 0
				&& ed.selection.getRng(true).startContainer.parentElement.nodeName == 'SPAN') {
					e.preventDefault();
					e.stopPropagation();
					console.log('cursor leaving SPAN keyup');
			}*/
	
			loadEditorToBox(edCurrentTarget);
		});

		ed.onKeyDown.add(function(ed, e) {

			/*if (e.keyCode == KEYLEFT 
				&& ed.selection.isCollapsed() 
				&& ed.selection.getRng(true).startOffset == 1 
				&& ed.selection.getRng(true).startContainer.parentElement.nodeName == 'SPAN') {
					e.preventDefault();
					e.stopPropagation();
					console.log('cursor left leaving SPAN keydown');
					//var rng = ed.selection.getRng(true);
					//rng.setStart(rng.startContainer, 0);
					//rng.collapse(true);
			} else if (e.keyCode == KEYRIGHT
				&& ed.selection.isCollapsed() 
				&& ed.selection.getRng(true).startOffset == ed.selection.getRng(true).startContainer.nodeValue.length
				&& ed.selection.getRng(true).startContainer.parentElement.nodeName == 'SPAN') {
					e.preventDefault();
					e.stopPropagation();
					console.log('cursor right leaving SPAN keydown');
			}*/
	
			// Prevent carriage return in box. tinyMCE gets overactive with the <br /> if you don't.
			if (ed.dom.hasClass(ed.selection.getNode(), 'eqn')) {
				
				switch (e.keyCode) {
					case 13:
						// Prevent enter key in equations
						e.preventDefault();
						e.stopPropagation();
						break;
				}
			}
		});
            }
    });     
    textEd.render();
    hideEditor();
}

// Content box to editor conversion
// Copies content box, rips out any display mathjax (leaving script elements behind), converts script elements to spans.
function loadBoxToEditor(target) {

    var tbox_contents = target.children(".textbox").clone();
    tbox_contents.find('.MathJax_Display').remove();
    tbox_contents.find('.MathJax').remove();
    tbox_contents.find('script').replaceWith(function() {
	var newSpan = $('<span></span>');
	newSpan.attr('id', $(this).attr('id'));
        newSpan.addClass('eqn');
	if ($(this).attr('type') == "math/tex; mode=display") {
		newSpan.addClass('display');
	} else if ($(this).attr('type') == "math/tex; mode=inline") {
		newSpan.addClass('inline');
	} else {
		throw "Mangled MathJax type attribute: " + $(this).attr('type');
	} 
	newSpan.html($(this).text());
	return newSpan;
    });
    textEd.setContent(tbox_contents.html());

}

// Copies editor contents to specified box
// Reverse loadBoxToEditor: replace spans with scripts (decoding html entities) and re-typeset.
function loadEditorToBox(target) {

	editorContents = $('<div />').html($(textEd.getContent()).clone());
	editorContents.find('span.eqn').replaceWith(function() {
		var display = $(this).hasClass('display') ? 'display' : 'inline';
		var newScript = $('<script type="math/tex; mode=' + display + '"></script>');
		newScript.attr('id', $(this).attr('id'));
		newScript.text($(this).html());
		return newScript;
	});
	target.children(".textbox").html(editorContents.html());
	MathJax.Hub.Queue(["Typeset", MathJax.Hub, target.children(".textbox").get(0)]);
}

function showEditor(target) {
    edCurrentTarget = target;
    textEd.setContent('<p></p>');
    $('#textEditorContainer').slideDown('1000');
    textEd.setProgressState(1);
    loadBoxToEditor(target);
    textEd.setProgressState(0);
    textEd.focus();
}

function hideEditor() {
    edCurrentTarget = false;
    $('#textEditorContainer').slideUp('1000');
}

function saveEditor() {
    if (edCurrentTarget == false) {
	// Not currently editing, abort quietly
	return;
    }
    loadEditorToBox(edCurrentTarget);
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
    // Saving - like boxToEditor, but keep script tags (remove ids so they are auto-generated each time page is loaded)
    var boxContent = $(edCurrentTarget).children(".textbox").clone();
    boxContent.find('.MathJax_Display').remove();
    boxContent.find('.MathJax').remove();
    boxContent.find('script').removeAttr('id');
    bb.append(boxContent.html());
    var blob = bb.getBlob('text/html');
    content.handleSaveContent(pageID, edCurrentTarget.attr("id").replace('c',''), blob, { name:'textbox'+edCurrentTarget.attr("id").replace('c','')+'.html', type:'text/html', size: blob.size });
    textEd.setProgressState(0);
}
