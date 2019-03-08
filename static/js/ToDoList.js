$(document).ready(function() {
    //Reads from the sql database on my laptop whenever the page is loaded
    $.get('/todo/read', function(data) {
        for (var i in data) {
            //Creates delete button within a variable 
            var xbutton = $("<span>").addClass("close").text("\u00D7").click(function() {
                //Gives the deleted data to flask/python setup
                $.ajax({
                     type: "DELETE",
                     url: "/todo/delete",
                     data: {
                         dataItem : $(this).parent().text(),
                         index : $(this).parent().index().valueOf(),
                         dataSize : $( "li" ).length
                     },
                     success: function() {
                     }
                });
                $(this).parent().remove();
            });
            //Makes an element that has the text and aformentioned cancel button
            var elem = $("<li>").addClass("list-group-item list-group-item-action")
                                .text(data[i])
                                .append(xbutton);
            //Adds entry to front end list
            $("#todo-list").append(elem);
        }
    });
    
    //Performs the search whenever the search bar is keyed into
    $("#search").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        for (i = 0; i < $( "li" ).length; i++) {
            if ($("#todo-list").children().eq(i).text().toLowerCase().indexOf(value) > -1) {
                console.log($("#todo-list").children().eq(i).text());
                $("#todo-list").children().eq(i).show();
            }
            else
                $("#todo-list").children().eq(i).hide();
        }
    });
    
    //Clears out the list as well as the native sql database
    $("#clear").click(function(e) {
        e.preventDefault();
        //Has a request but doesn't give any significant data
        $.ajax({
             type: "DELETE",
             url: "/todo/clear",
             data: 0,
             success: function() {
             }
         });
        $("#todo-list").children().remove();
    });
    
    //Updates an individual data entry whenever update is pressed
    $("#update").click(function(e) {
        e.preventDefault();
        //Creates delete button within a variable 
        var xbutton = $("<span>").addClass("close").text("\u00D7").click(function() {
            //Gives the deleted data to flask/python setup
            $.ajax({
                 type: "DELETE",
                 url: "/todo/delete",
                 data: {
                     dataItem : $(this).parent().text(),
                     index : $(this).parent().index().valueOf(),
                     dataSize : $( "li" ).length
                 },
                 success: function() {
                 }
            });
            $(this).parent().remove();
        });
        //Gives the updated data to flask/python setup
        $.ajax({
            type: "PUT",
            url: "/todo/update",
            data: {
                 index : ($("#num").val()-1),
                 updateTxt: $("#myInput").val()
             },
            success: function(response) {
                console.log(response);
            }
        });
           
        //Peforms the front-end replacing of elements
        $("#todo-list").children().eq($("#num").val()-1).text($("#myInput").val()).append(xbutton);
    });
    
    //Adds items to the list
    $("#btn").click(function(e) {
        e.preventDefault();
        //Creates delete button within a variable 
        var xbutton = $("<span>").addClass("close").text("\u00D7").click(function() {
            //Gives the deleted data to flask/python setup
            $.ajax({
                 type: "DELETE",
                 url: "/todo/delete",
                 data: {
                     dataItem : $(this).parent().text(),
                     index : $(this).parent().index().valueOf(),
                     dataSize : $( "li" ).length
                 },
                 success: function() {
                 }
            });
            $(this).parent().remove();
        });
        //Makes an element that has the text and aformentioned cancel button
        var elem = $("<li>").addClass("list-group-item list-group-item-action")
                            .text($("#myInput").val())
                            .append(xbutton);
        //Connects with flask and sends its data to python when the Add Item button is pressed
        $.ajax({
            type: "POST",
            url: "/todo/create",
            data: $("#myInput").serialize(),
            success: function(response) {
                $("#todo-list").append(elem);
                $("#myInput").val();
            }
        });
    });
});