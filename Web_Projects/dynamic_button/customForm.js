$(document).ready(function(){
    var currentId="s1";
    var searches = {};
    searches["s1"] = {};
    searches["s2"] = {};   
    var lastId = 1;
    $('#btnAdd').on("click",function (e) {
    lastId = lastId+1;
    var nextTab = lastId+1;

    
    // create the tab
        $('<li><a href="#" class = "new-search" id = "s'+nextTab+'">Search#'+nextTab+'</a><span secondary-id = "s' +nextTab +'" class="glyphicon glyphicon-remove close-button" aria-hidden="true"></span></li>').appendTo('#searches');
        $('#searches a:last').tab('show');
        var newId = $('#searches a:last').prop('id');
        console.log("new id is " + newId);
        searches[newId] = {};
        currentId = newId;
        console.log("therefore the current id is set to" + currentId);
    });

    $("#update_button").on("click",function(){
        console.log(searches[currentId]);
        searches[currentId].val1 = $("input[name^='selectors']")[0].checked;
        searches[currentId].val2 = $("input[name^='selectors']")[1].checked;
        searches[currentId].val3 = $("input[name^='selectors']")[2].checked;
        searches[currentId].val4 = $("input[name^='selectors']")[3].checked;
        console.log(searches[currentId]);
    });

    $("#searches").on("click", ".close-button",function(event){
        console.log("current id before deleting the button is " + currentId);
        closedId = $(event.target).attr('secondary-id');
        $('#'+closedId).parent().remove();
        console.log("close button clicked and the id of the close button clicked is " +closedId);
        delete(searches[closedId]);

        if (currentId == closedId){
            var keyArray = Object.keys(searches);
            var len = keyArray.length;
            if (len==0){
                currentId = undefined;
                $("input[name^='selectors']")[0].checked = false;
                $("input[name^='selectors']")[1].checked = false;
                $("input[name^='selectors']")[2].checked = false;
                $("input[name^='selectors']")[3].checked = false;                   
            } else {
                currentId = keyArray[len-1];
                var currentCriteria = searches[currentId];
                $("input[name^='selectors']")[0].checked = currentCriteria.val1;
                $("input[name^='selectors']")[1].checked = currentCriteria.val2;
                $("input[name^='selectors']")[2].checked = currentCriteria.val3;
                $("input[name^='selectors']")[3].checked = currentCriteria.val4;                
            }
        } 
        console.log("after deleting, the new current id is " + currentId);
            //reset currentId to a default
            

        //update all fields basing on current id
    });
    $("#searches").on("click", "a",function(event){
        // let the check boxes show the value in this object
        currentId = $(event.target).attr('id');
        console.log(searches[currentId]);
        console.log("now we should update the current criteria of id = " + currentId);
        if (searches[currentId]!=undefined){
            var currentCriteria = searches[currentId];
            $("input[name^='selectors']")[0].checked = currentCriteria.val1;
            $("input[name^='selectors']")[1].checked = currentCriteria.val2;
            $("input[name^='selectors']")[2].checked = currentCriteria.val3;
            $("input[name^='selectors']")[3].checked = currentCriteria.val4;
        } else {
            // clear fields
            $("input[name^='selectors']")[0].checked = false;
            $("input[name^='selectors']")[1].checked = false;
            $("input[name^='selectors']")[2].checked = false;
            $("input[name^='selectors']")[3].checked = false;            
        }

    });


	$("#search_button").click(function(){
        console.log(JSON.stringify(searches));


    });
	$("#myModal").on('hidden.bs.modal', function (e) {

        $("#start").val("");
        $("#end").val("");
        $("#congress").val("114");
        $.each($("input[name='selectors']:checked"), function() {
          $(this).removeAttr('checked');
        });
        $.each($("input[name='from']:checked"), function() {
          $(this).removeAttr('checked');
        });
        $("#allAvailable").attr('checked') = 'checked';           
        console.log("modal closed, all fields have been reset");        
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


