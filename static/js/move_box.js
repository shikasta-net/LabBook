jQuery(document).ready(function(){
    var pxPerem = $("div.page").width()/70.0
    $(".txtbox").disableSelection();
    $(".txtbox").draggable({

        // Find original position of dragged image.
        //start: function(event, ui) {
    
            // Show start dragged position of image.
            //var Startpos = $(this).offset();
            //$("div#start").text("START: \nLeft: "+ (Startpos.left - $("div.page").offset().left)/pxPerem + "\nTop: " + (Startpos.top - $("div.page").offset().top)/pxPerem);
       // },
    
        // Find position where image is dropped.
        stop: function(event, ui) {
            var Stoppos = $(this).offset();
            var tbid = $(this).attr("id").replace('tb','');
            //$.get('http://127.0.0.1:8000/LabBook/default/call/run/moved?id='+tbid+'&x='+(Stoppos.left - $("div.page").offset().left)/pxPerem+'&y='+(Stoppos.top - $("div.page").offset().top)/pxPerem);
            //$.get('http://127.0.0.1:8000/LabBook/default/call/run/moved?id='+tbid+'&x='+(Stoppos.left - $("div.page").offset().left)/pxPerem+'&y='+(Stoppos.top - $("div.page").offset().top)/pxPerem);
            
            // Show dropped position.
           // var Stoppos = $(this).offset();
           // $("div#stop").text("element " + tbid + " STOP: \nLeft: "+ (Stoppos.left - $("div.page").offset().left)/pxPerem + "\nTop: " + (Stoppos.top - $("div.page").offset().top)/pxPerem);
        },
     snap: ".snapable", snapTolerance: 5 });
    $(".txtbox").resizable();
});
