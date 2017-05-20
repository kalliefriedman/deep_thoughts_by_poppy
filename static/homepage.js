"use strict";

$(document).ready(function(){

// on form submit, returns a new machine-generated tweet
    $("#submit").click(function(evt){
        evt.preventDefault();
        var handle = $("#handle").val();
        //pack up the form values into an object
        var formData = {"handle": handle};
        
        //make the AJAX request and append response to DOM
        $.post("/generate-new-tweet.json", formData, function(results) {
                $("#newtweet").empty();
                
                if (results){
                    $("#newtweet").append("<b>Poppy's recent thinking: </b><br/><br/>");
                    $("#newtweet").append(results);
                    $("#newtweet").append('<br/>'); 
                }

                else {
                    $("#newtweet").append("There was a problem with the user you've identified. Please try again.");
                    }
                                        }); // end of post request

        //make the AJAX request and append response to DOM
        $.get("/get-past-tweets.json", formData, function(results) {
                     $("#pasttweets").empty();
                     if (results){
                        if (results.length > 1){
                     $("#pasttweets").append("<b>Poppy's prior deep thinking: </b>");
                     $("#pasttweets").append('<br/><br/>'); 
                  
                     for (var i = 0; i < results.length-i; i++) {
                        $("#pasttweets").append(results[i] + '<br/><br/>');
                        } //end of forloop

                    } //end of if statement

                                        } //end of second if statement
                                        
                                        }); //end of get request 

                                        });  //end of event listener click function
                                        }); //end of document.ready