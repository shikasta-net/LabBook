var crossBoxCounter = 0;

function crossBox(css) {

    crossBoxCounter++;
    this.crossBoxID = crossBoxCounter;
    this.crossDiv = $('<div class="crossbox" id="crossbox' + crossBoxCounter + '"></div>');
    this.line1 = $('<div class="line"></div>');
    this.line2 = $('<div class="line"></div>');
    this.crossDiv.append(this.line1);
    this.crossDiv.append(this.line2);

    if (css != undefined) {
        this.crossDiv.css(css);
    }
    this.elementOver = false;
    this.crossDiv.on('dragleave', null, {crossBox: this},
        function(event) {
            thisCrossBox = event.data.crossBox;
            event = event.originalEvent;
            if(event.target.id == "crossbox" + thisCrossBox.crossBoxID) {
                if(!($(event.relatedTarget).hasClass('line'))) {
                    thisCrossBox.hide()
                    thisCrossBox.elementOver = false;
                }
            }
        });
                                                    
    this.crossDiv.on('drop', null, {crossBox: this},
	    function(event) {
	    	event.preventDefault();
	    	event.stopPropagation(); 
            	thisCrossBox = event.data.crossBox;
		event = event.originalEvent;
		if (event.target.id == "crossbox" + thisCrossBox.crossBoxID) {
		    if (!($(event.relatedTarget).hasClass('line'))) {
		    	thisCrossBox.hide();
            		content.handleDrop(event);
            		thisCrossBox.elementOver = false;
		    }
		}
            });
    
    this.crossDiv.on('dragover', function (event) {
        event.stopPropagation();
        event.preventDefault();
        event.originalEvent.dataTransfer.dropEffect = 'copy';
    });

    this.resizeAndPosition = function(newElementID) {

        var crossElement = $('#'+newElementID);
        var x = crossElement.position().left;
        var y = crossElement.position().top;
        var w = crossElement.width();
        var h = crossElement.height();
        var borderWidthAdjust = (this.crossDiv.innerWidth() - this.crossDiv.outerWidth()) - (crossElement.innerWidth() - crossElement.outerWidth());
        var borderHeightAdjust = (this.crossDiv.innerHeight() - this.crossDiv.outerHeight()) - (crossElement.innerHeight() - crossElement.outerHeight());
        var hypotenuse = Math.sqrt(Math.pow(w+borderWidthAdjust, 2) + Math.pow(h+borderHeightAdjust, 2));
        var angle = Math.atan2(h+borderHeightAdjust, w+borderHeightAdjust) * 180.0/Math.PI;
        this.crossDiv.width(w+borderWidthAdjust);
        this.crossDiv.height(h+borderHeightAdjust);

        this.line1.css({
            'transform': 'rotate('+angle+'deg)',
            '-moz-transform': 'rotate('+angle+'deg)',
            '-webkit-transform': 'rotate('+angle+'deg)'})
            .width(hypotenuse);

        this.line2.css({
            'transform': 'rotate(-'+angle+'deg)',
            '-moz-transform': 'rotate(-'+angle+'deg)',
            '-webkit-transform': 'rotate(-'+angle+'deg)',
            'top': h+borderHeightAdjust})
            .width(hypotenuse);

        elementOffset = crossElement.offset();

        this.crossDiv.css({
            'top': crossElement.css('top'),
            'left': crossElement.css('left')
        });
    }

    this.show = function() {
        this.crossDiv.fadeIn(100);
    }

    this.hide = function() {
        this.crossDiv.fadeOut(100);
    }

}
