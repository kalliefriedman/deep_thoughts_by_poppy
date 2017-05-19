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
                    $("#newtweet").append("Poppy's recent thinking: ");
                    $("#newtweet").append(results);
                    $("#newtweet").append('<br/><br/>'); 
                }

                else {
                    $("#newtweet").append("There was a problem with the user you've identified. Please try again.");
                    }
                                        }); // end of post request

        $.get("/get-past-tweets.json", formData, function(results) {
                     console.log(results);
                     $("#pasttweets").empty();
                     $("#pasttweet").append("Poppy's prior deep thinking: ");
                                        
                                         for (var tweet in results) {
                                            $("#pasttweets").append(tweet + '<br/><br/>');
                                            } //end of forloop
                                        }); //end of get request                              
                                        } 
                                        ); 
                                        }); //end of document.ready