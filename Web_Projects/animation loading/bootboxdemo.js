$(document).ready(function(){
    $("#fillOutFormButton").click(function(){
    console.log("button clicked");
    bootbox.dialog({
    title: "Alternative approaches for \"System Busy\" dialog",
    onEscape: function(){},
    message:'<div class = "container">' + 
    		'<h4>This is a customized gif image</h4>'+
    		'<img src="322.gif" width="50px"/></div>'+
    		'<div class = "container">'+
    		'<h4>This is a spinner animation from font awesome</h4>'+
    		'<font size="6"><i class = "fa fa-spinner fa-spin"></i></font></div>'
        });
    });
});



