"use strict";

$(document).ready(function(){

// prevents default and makes call to get-tweets, constructing URL, on click
    $("#submit").click(function(evt){
        evt.preventDefault();
        var handle = $("#handle").val();
        //pack up the form values into an object
        var formData = {"handle": handle};

        //make the AJAX request and append response to DOM
        $.post("/get-tweets", formData, function(results) {
    
        
                                                var tagId = results.tag_id;
                                                var articleId = results.article_id;
                                                var tagValue = results.tag_value;

                                                var newForm = $("<form>");
                                                newForm.attr("id", "tag-id-" + tagId);
                                                newForm.attr("class", "delete-tag");
                                                
                                                var articleIdInput = $("<input>");
                                                articleIdInput.attr("type", "hidden");
                                                articleIdInput.attr("name", "article_id");
                                                articleIdInput.attr("value", articleId);
                                                $(newForm).append(articleIdInput);

                                                var tagIdInput = $("<input>");
                                                tagIdInput.attr("type", "hidden");
                                                tagIdInput.attr("name", "tag_id");
                                                tagIdInput.attr("value", tagId);
                                                $(newForm).append(tagIdInput);

                                                var submitInput = $("<input>");
                                                submitInput.attr("class", "filter");
                                                submitInput.attr("type", "submit");
                                                submitInput.attr("name", "tag_value");
                                                submitInput.attr("value", tagValue + " x");
                                                $(newForm).append(submitInput);

                                                newForm.append(newForm);
                                                $("#tags").append(newForm);
                                                
                                                } //end of callback function
        ); //end of AJAX request
    } //end of tagadd