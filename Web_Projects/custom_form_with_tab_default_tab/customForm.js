$(document).ready(function(){
	var activeTab = "#tab_one";//default active tab
	$(".nav-tabs a").on("shown.bs.tab",function(event){
		activeTab = $(event.target).attr("href");
        console.log("current active tab is " + activeTab);

	});
    $("#two").click(function(){
        console.log("right button clicked");
        activeTab = "#tab_two";
        $("#tabs li:nth-child(1)").attr("class","");
        $("#tabs li:nth-child(2)").attr("class","active");
        $("#tab_one").removeClass("in active");
        $("#tab_two").addClass("in active");
        $("#myModal").modal();
    });

    $("#one").click(function(){
        console.log("left button clicked");
        activeTab = "#tab_one";
        $("#tabs li:nth-child(2)").attr("class","");
        $("#tabs li:nth-child(1)").attr("class","active");
        $("#tab_two").removeClass("in active");
        $("#tab_one").addClass("in active");
        $("#myModal").modal();
    });




	$("#search_button").click(function(){
    	if (activeTab=="#tab_one"){
            var name = $("#name").val();
            var sex = $("input[name='sex']:checked").val();
            $("#result").html("Your search criteria are " + name + " and " + sex);		
    	}
    	else {
    		var id = $("#ID").val();
            $("#result").html("Your search criteria is ID = " + id);	    		
    	}

    });
	$("#cancel_button").click(function(){
    	console.log("cancel button clicked");
  	});
	$("#myModal").on('hidden.bs.modal', function (e) {
        console.log("modal closed. all fields have been rest");
  		$("#name").val("");
    	$("#ID").val("");
    	$("#male").prop("checked",true);
    	$("#female").prop("checked",false);
	})
    $("#myModal").keypress(function(e){
        if (e.which == '14'){
            if (activeTab=="#tab_one"){
                var name = $("#name").val();
                var sex = $("input[name='sex']:checked").val();
                $("#result").html("Your search criteria are " + name + " and " + sex);      
            }
            else {
                var id = $("#ID").val();
                $("#result").html("Your search criteria is ID = " + id);                
            }
        }
    });
});


