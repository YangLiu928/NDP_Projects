$(document).ready(function(){
	
    var activeTab = "#tab_one";
	
    $(".nav-tabs a").on("shown.bs.tab",function(event){
		activeTab = $(event.target).attr("href");
        console.log("current active tab is " + activeTab);

	});

	$("#search_button").click(function(){
    	if (activeTab=="#tab_one"){
            var name = $("#name").val();
            xmlhttp = new XMLHttpRequest({mozSystem: true});
            xmlhttp.onreadystatechange = function(){
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                    console.log("I got the response");
                document.getElementById("results").innerHTML = xmlhttp.responseText;
                }
            };
            xmlhttp.open("GET","http://localhost/getschool.php?name="+name,true);
            console.log("name= " + name);
            xmlhttp.send();	
    	}
    	else {
    		var state = $("#state").val();
                        xmlhttp = new XMLHttpRequest({mozSystem: true});
            xmlhttp.onreadystatechange = function(){
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                    console.log("I got the response");
                document.getElementById("results").innerHTML = xmlhttp.responseText;
                }
            };
            xmlhttp.open("GET","http://localhost/getschool.php?state="+state,true);
            console.log("state= " + state);
            xmlhttp.send();	    		
    	}

    });

	$("#cancel_button").click(function(){
    	console.log("cancel button clicked");
  	});

	$("#myModal").on('hidden.bs.modal', function (e) {
        console.log("modal closed. all fields have been rest");
  		$("#name").val("");
    	$("#state").val("");
        $("#results").text("");
	})
    $(document).on('click','.description_page',function(){
        console.log('You clikced a school');
        console.log($(this));
        $("#selected_result").html("You have selected " + $(this).text());       
    });
});


