function createDiv()
    {
        var divTag = document.createElement("div");        
               
        divTag.id = "div1";
                
        divTag.style = "position:relative;left:2em;top:2em;width:10em;height:10em;";
        
        divTag.className ="txtbox";
        
        divTag.innerHTML = "This HTML Div tag created using Javascript DOM dynamically.";
        
        document.getElementById('main_page').appendChild(divTag);
    }
