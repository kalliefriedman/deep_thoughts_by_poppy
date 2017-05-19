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
                console.log(results);
                $("#newtweet").empty();
                
                if (results){
                    $("#newtweet").append("Poppy's recent thinking: ");
                    $("#newtweet").append(results);
                }

                else {
                    $("#newtweet").append("There was a problem with the user you've identified. Please try again.");
                    }
                                        }); // end of post request

        // $.get("//get-past-tweets.json", formData, function(results) {
        //                                     console.log(results);
        //                                     $("#newtweet").append(results);
        //                                 }
        //                                 ); //end of get request                              

                                        } 
                                        ); 
                                        }); //end of document.ready