$(document).ready(function(){
    $("#start").datepicker({ 
        autoclose: true, 
        todayHighlight: true,
        orientation: "auto",
        todayBtn: "linked",
        clearBtn: true
    });
    $("#end").datepicker({ 
        autoclose: true, 
        todayHighlight: true,
        orientation: "auto",
        todayBtn: "linked",
        clearBtn: true
    });


    $(".congress").click(function(){
        console.log($(this).text());
        console.log($("#congress-button").textContent);
        $("#congress_button").html = $(this).text();
    });



	$("#search_button").click(function(){



        var keywords = $("#keywords").val();
        $("#keywords").val("");

        var from = new Array();
        $.each($("input[name='from']:checked"), function() {
          from.push($(this).val());
          $(this).removeAttr('checked');
        });


        var selectors = new Array();
        $.each($("input[name='selectors']:checked"), function() {
          selectors.push($(this).val());
          $(this).removeAttr('checked');
        });

        var period = $("input[name=period]:checked").val()

        if (period=="allAvailable"){
            period = "allAvailable";
        } else if (period=="dateRange"){
            period = "from " + $("#start").val() + " to " + $("#end").val();
        } else {
            period = $("#congress").find(":selected").text();
        }
        $("#start").val("");
        $("#end").val("");
        $("#congress").val("114");


        $("#result").html(
            "Your search criteria are: <br>" + 
            "include votes of: " + period + "<br>"+
            "include vote from: " + from + "<br>" +  
            "include vote with the following title: " + keywords + "<br>" + 
            "include votes about: " + selectors
            );


    });
	$("#cancel_button").click(function(){
    	console.log("cancel button clicked");
  	});
	$("#myModal").on('hidden.bs.modal', function (e) {
    //     console.log("modal closed. all fields have been rest");
  		// $("#name").val("");
    // 	$("#ID").val("");
    // 	$("#congress").prop("checked",false);
    //     $("#keywords").val("");
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


