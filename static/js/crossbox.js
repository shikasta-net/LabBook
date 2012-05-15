var crossBox = $('<div id="crossbox"></div>');
var crossLine1 = $('<div class="line" id="line1"></div>');
var crossLine2 = $('<div class="line" id="line2"></div>');
crossBox.append(crossLine1);
crossBox.append(crossLine2);
crossBox[0].addEventListener('dragleave', function(event) {
                                                event = event || window.event;
                                                if(event.target.id == "crossbox") {
                                                    if(!(event.relatedTarget.id == "line1"
                                                        || event.relatedTarget.id == "line2")) {

                                                        crossBoxHide();
                                                        crossBoxOver = false;
                                                        
                                                    }
                                                }});
                                                    
crossBox[0].addEventListener('drop', function(event) { crossBoxHide(); handleDrop(event); crossBoxOver = false});
crossBox[0].addEventListener('dragover', function (event) { handleDragOver(event) });

function handleDragOver(event) {
    event.stopPropagation();
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
}

function crossBoxResizeAndPosition(crossElementID) {

    var crossElement = $('#'+crossElementID);
    var hypotenuse = Math.sqrt(Math.pow(crossElement.width(), 2) + Math.pow(crossElement.height(), 2));
    var angle = Math.atan2(crossElement.height(), crossElement.width()) * 180.0/Math.PI;
   
    crossBox.width(crossElement.width())
                .height(crossElement.height());

    
    crossLine1.css({
        'transform': 'rotate('+angle+'deg)',
        '-moz-transform': 'rotate('+angle+'deg)', 
        '-webkit-transform': 'rotate('+angle+'deg)'})
        .width(hypotenuse);
        
    crossLine2.css({
        'transform': 'rotate(-'+angle+'deg)', 
        '-moz-transform': 'rotate(-'+angle+'deg)', 
        '-webkit-transform': 'rotate(-'+angle+'deg)', 
        'top': crossElement.height()})
        .width(hypotenuse);

    elementOffset = crossElement.offset();

    crossBox.css({
            'top': crossElement.css('top'),
            'left': crossElement.css('left')
            });

}
   
function crossBoxHide() {
    crossBox.fadeOut(100);
}

function crossBoxShow() {
    crossBox.fadeIn(100);
}

var crossBoxOver = false;

function getCrossBox() { return crossBox; }