$(document).ready(function(){
	$("#YesButton").click(function(){
    	console.log('Yes Button clicked');
    	$("#result").html("yes button clicked");
    });
	$("#NoButton").click(function(){
    	console.log('No Button clicked');
    	$("#result").html("no button clicked");
  });	
});


