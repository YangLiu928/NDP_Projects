$(document).ready(function(){
	var activeTab = "#tab_one";//default active tab
	$(".nav-tabs a").on("shown.bs.tab",function(event){
		activeTab = $(event.target).attr("href");
        console.log("current active tab is " + activeTab);

	});
	$("#search_button").click(function(){
    	if (activeTab=="#tab_one"){
            var name = $("#name").val();
            var sex = $("input[name='sex']:checked").val();
            xmlhttp = new XMLHttpRequest({mozSystem: true});
            xmlhttp.onreadystatechange = function(){
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                    console.log("I got the response");
                    console.log("The response is " + xmlhttp.responseText);
                document.getElementById("result").innerHTML = xmlhttp.responseText;
                }
            };


            xmlhttp.open("GET","file://localhost/testmysql.php?"+name,true);
            xmlhttp.send();
     //        $("#result").html("Your search criteria are " + name + " and " + sex);		
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
    $("#description_page").click(function(){
        
    });
});


