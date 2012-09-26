var textEd = false;
var edCurrentTarget = false;
var KEYLEFT = 37;
var KEYRIGHT = 39;
var DOLLAR = 36;
var CTRLDOLLAR = 52;

function initialiseEditor() {
	$('body').append("<div class='claro' id='textEditorContainer'><div id='textEditor'></div></div>");
	require(["dijit/Editor",
		"dojo/parser",
		"dojo/domReady!",
		"dijit/_editor/plugins/FontChoice",
		"dijit/_editor/plugins/LinkDialog",
		"dojox/editor/plugins/TextColor"
		// ,
		// "dojox/editor/plugins/TablePlugins",
		// "dojox/editor/plugins/ResizeTableColumn"
		],
		function(Editor){
			textEd = new Editor({
				plugins: ["bold","italic","|","cut","copy","paste","|","insertUnorderedList"
					// ,"|",
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'insertTable'},
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'modifyTable'},
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'InsertTableRowBefore'},
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'InsertTableRowAfter'},
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'insertTableColumnBefore'},
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'insertTableColumnAfter'},
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'deleteTableRow'},
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'deleteTableColumn'},
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'colorTableCell'},
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'tableContextMenu'},
					// {name: 'dojox.editor.plugins.TablePlugins', command: 'ResizeTableColumn'}
				],
				extraPlugins : ["fontName","fontSize","formatBlock","foreColor","hiliteColor","|","createLink"],
				setupDefaultShortcuts: function(){}
			}, "textEditor");

			textEd.addStyleSheet("/LabBook/static/css/page_css.css");

			textEd.connect(textEd, "onKeyPress", function(e){
				// If we're currently editing an equation...
				//textEd.window probably only works outside IE
				caretNode = textEd.window.getSelection().anchorNode.parentNode;
				if ($(caretNode).hasClass('eqn')) {
					// Pressed $ in inline eqn? Boost eqn to display
					if (e.charCode == DOLLAR && $(caretNode).hasClass('inline')) {
						e.preventDefault();
						e.stopPropagation();
						$(caretNode).removeClass('inline');
						$(caretNode).addClass('display');
					}
					// Pressed Ctrl-$ in inline? Remove eqn and leave plaintext
					if (e.charCode == CTRLDOLLAR && $(caretNode).hasClass('inline')) {
						e.preventDefault();
						e.stopPropagation();
						var temp = $(caretNode).html();
						$(caretNode).remove();
						textEd.execCommand('inserthtml', temp);
						//textEd.window.getSelection().deleteFromDocument();
						//textEd.window.getSelection().anchorNode.parentNode.innerHTML(temp);
					}
					// Pressed Ctrl-$ in inline? Ignore
					if (e.charCode == DOLLAR && $(caretNode).hasClass('display')) {
						e.preventDefault();
						e.stopPropagation();
					}
					// Pressed Ctrl-$ in display eqn? Reduce to inline eqn
					if (e.charCode == CTRLDOLLAR && $(caretNode).hasClass('display')) {
						e.preventDefault();
						e.stopPropagation();
						$(caretNode).removeClass('display');
						$(caretNode).addClass('inline');
					}

				} else {
					// $ pressed outside equation? Make new eqn.
					if (e.charCode == DOLLAR) {
						e.preventDefault();
						e.stopPropagation();
						var eqnIDCounter = 0;
						while ($('#eqn_' + eqnIDCounter).get(0)) { eqnIDCounter++; }
						var newEqn = textEd.document.createElement('span');
						$(newEqn).attr('id', 'eqn_' + eqnIDCounter);
						$(newEqn).addClass('eqn inline');
						console.log($('<p></p>').append(newEqn).html());
						var convert = !textEd.window.getSelection().isCollapsed;
						if (convert) {
							textEd.window.getSelection().getRangeAt(0).surroundContents(newEqn);
						} else {
							var newnode = textEd.document.createTextNode(" ");
							newEqn.appendChild(newnode);
						}
						textEd.execCommand("inserthtml", "&nbsp;" + $('<p></p>').append(newEqn).html() + "&nbsp;");
						var rng = textEd.document.createRange();
						var eqnID = textEd.document.getElementById("eqn_" + eqnIDCounter);
						if (convert) {
							rng.selectNodeContents(eqnID);
							rng.collapse(false);
						} else {
							rng.setStart(eqnID.childNodes[0],0);
							rng.setEnd(eqnID.childNodes[0],1);
						}
						var sel = textEd.window.getSelection();
						sel.removeAllRanges();
						sel.addRange(rng);
						// ed.selection.setNode(newEqn);
						// ed.selection.select(ed.dom.select('#'+newEqnID)[0].firstChild);
					}
				}


			});
			// Update content box every time user presses a key.
			// TODO: Less intensive update scheme? (eg track caret position and update only updated elements?) Complicated!
			textEd.connect(textEd, "onKeyUp", function(e){

/*				if (e.keyCode == KEYLEFT
					&& ed.selection.isCollapsed()
					&& ed.selection.getRng(true).startOffset == 0
					&& ed.selection.getRng(true).startContainer.parentElement.nodeName == 'SPAN') {
						e.preventDefault();
						e.stopPropagation();
						console.log('cursor leaving SPAN keyup');
				}*
*/
				loadEditorToBox(edCurrentTarget);
			});
			textEd.connect(textEd, "onKeyDown", function(e){
/*
				if (e.keyCode == KEYLEFT
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

				// Prevent carriage return in box. Dojo gets overactive with the <br /> if you don't.
				if ($(textEd.window.getSelection().anchorNode.parentNode).hasClass('eqn')) {

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
	);
	hideEditor();
}

// Content box to editor conversion
// Copies content box, rips out any display mathjax (leaving script elements behind), converts script elements to spans.
function loadBoxToEditor(target) {
    if (target.children('.textbox').length != 1) {
        throw "loadBoxToEditor called on container which doesn't have only one textbox";
    }
	var tbox_contents = $(target.children('.textbox')[0]).clone();
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
	textEd.set("value",tbox_contents.html());
	textEd.focus();
}

// Copies editor contents to specified box
// Reverse loadBoxToEditor: replace spans with scripts (decoding html entities) and re-typeset.
function loadEditorToBox(target) {

	editorContents = $('<div />').html(textEd.get("value"));
	editorContents.find('span.eqn').replaceWith(function() {
		var display = $(this).hasClass('display') ? 'display' : 'inline';
		var newScript = $('<script type="math/tex; mode=' + display + '"></script>');
		newScript.attr('id', $(this).attr('id'));
		newScript.text($(this).text());
		return newScript;
	});
	$(target).children('.textbox.').html(editorContents.html());
	MathJax.Hub.Queue(["Typeset", MathJax.Hub, target.children(".textbox").get(0)]);
}

function showEditor(target) {
	edCurrentTarget = target;
	edCurrentTarget.append('<div style="background-color: black; color: white; font-family: sans-serif; width: 6em; height: 1em;" id="preview">Preview</div>');
	$('#preview').position({ my: 'bottom right', at: 'bottom right', of: edCurrentTarget });
	textEd.set("value","<p></p>");
	$('#textEditorContainer').slideDown('1000');
	//~ textEd.setProgressState(1);
	if (target.hasClass('empty')) {
		console.log("Text editor called on something empty.");
		console.log(target);
		target.find('#option_bar').after("<div class='textbox' id='"+target.attr('id').replace('c','txt')+"'><p></p></div>");
		target.removeClass("empty");
		loadBoxToEditor(target);
	} else {
		loadBoxToEditor(target);
	} /*else {
		console.log("Text editor called on something which was neither a textbox nor empty.");
		textEd.setProgressState(0);
		hideEditor();
	}*/
	//~ textEd.setProgressState(0);
}

function hideEditor() {
	edCurrentTarget = false;
	$('#textEditorContainer').slideUp('1000');
	$('#preview').detach();
}

function saveEditor() {
	if (edCurrentTarget == false) {
	// Not currently editing, abort quietly
	return;
	}
	loadEditorToBox(edCurrentTarget);
	//~ textEd.setProgressState(1);
	// Saving - like boxToEditor, but keep script tags (remove ids so they are auto-generated each time page is loaded)
	var boxContent = $(edCurrentTarget).children(".textbox").clone();
	boxContent.find('.MathJax_Display').remove();
	boxContent.find('.MathJax').remove();
	boxContent.find('script').removeAttr('id');
	
	if (window.Blob) {
	   	var blob = new Blob([boxContent.html()], {type: 'text/html'});
	} else if (window.BlobBuilder) {
		var bb = new BlobBuilder();
	    bb.append(boxContent.html());
	    var blob = bb.getBlob('text/html');
	} else if (window.MozBlobBuilder) {
		var bb = new MozBlobBuilder();
		bb.append(boxContent.html());
	    var blob = bb.getBlob('text/html');
	} else if (window.MSBlobBuilder) {
		var bb = new MSBlobBuilder();
		bb.append(boxContent.html());
	    var blob = bb.getBlob('text/html');
	} else if (window.WebKitBlobBuilder) {
		var bb = new WebKitBlobBuilder();
		bb.append(boxContent.html());
	    var blob = bb.getBlob('text/html');
	} else {
		throw "No Blob or BlobBuilder implementation";
	}
	metadata = {name: 'text_' + edCurrentTarget.attr('id') + '.html', type: blob.type, size: blob.size}
	content.handleSaveContent(pageID, edCurrentTarget.attr("id"), blob, metadata);
	//~ textEd.setProgressState(0);
}
