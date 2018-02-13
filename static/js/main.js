/*variables*/
var ajax_loading = false;
var date_format = 'yy-mm-dd'

/*function: document ready*/
$(function() {
    ajax_loading = false;

    //0- add date ontrol
    $( "#picker-in" ).datepicker({ dateFormat: date_format });
    $( "#picker-out" ).datepicker({ dateFormat: date_format });

    // 1- add city auto complete
    autocomplete(document.getElementById("inp-dist"), city_list);

    // 2- handle search action

    // 2.1 search city
    $("#btn-search").click(function() {
        if (ajax_loading == true) {
            return;
        }

        // get selected country
        var dist = $('input#inp-dist').val();
        var checkin_value  = $( "#picker-in" ).val();
        var checkout_value = $( "#picker-out" ).val();

        if (dist != null && dist.trim() != "") {
            dist = dist.trim()
            call_search(dist, checkin_value, checkout_value)

        }

    })

    // 2.2 search offers without city
    $("#btn-lucky").click(function() {
        if (ajax_loading == true) {
            return;
        }

        call_search("","","")
    })

    //x- Control ajax loading
    $(document)
        .ajaxStart(function() {
            ajax_loading = true;

        })
        .ajaxStop(function() {
            ajax_loading = false;
        });

}); /*function: document ready*/

function get_advice(event) {
    var lat = $(event).data("lat")
    var lon = $(event).data("lon")

    var location = "( "+ lat+", "+lon +" )"
    alert("advice for location " + location)

}

function call_search(dist, checkin_value, checkout_value) {
    var form_data = new FormData()
    form_data.append("dist", dist);
    form_data.append("checkin", checkin_value);
    form_data.append("checkout", checkout_value);

    $.ajax({
        type: "POST",
        url: "hoteloffers",
        data: form_data,
        contentType: false,
        processData: false,
        success: function(response) {
            response = filter_result(response);
            display_results(response);
        },
        error: function(request, error) {
            response = $.parseJSON(request.responseText).message;
            show_dialog(response, "Error")
        }
    }); /*ajax*/
}

/*functions: controls*/
function filter_result(response) {
    return response;
}

function display_results(response) {
    //$('#div_result').html(response);

    if (response == null || response.length == 0) {
        show_intro()
        show_dialog("No result found", "Panda Advisor")
    } else {
        var response_json = JSON.parse(response)

        hide_intro()
        $('.card-columns').empty()

        offers_json = response_json['offer_list']
        if (offers_json != null ) {
            for (offer in offers_json) {
                console.log('hotel name: ' + offers_json[offer].hotel_name)

                // clone template div
                var current_card = $("#card-template").clone()
                var hotel_name = offers_json[offer].hotel_name

                current_card.removeAttr("id")
                // add image
                current_card.find("#card-image").attr("src", offers_json[offer].hotel_image);
                // add content
                current_card.find("#card-title").html(hotel_name);
                current_card.find("#card-text").html(offers_json[offer].hotel_destination);
                var stars_text = offers_json[offer].hotel_star + " / 5"
                current_card.find("#card-stars").html(stars_text);
                // add prices
                current_card.find("#old-price").html(offers_json[offer].original_price_night + "$");
                current_card.find("#new-price").html(offers_json[offer].average_price + "$");
                // add data to advice button (lat, long)
                current_card.find("#btn-panda").data("lat", offers_json[offer].hotel_lat);
                current_card.find("#btn-panda").data("lon", offers_json[offer].hotel_long);
                //update id
                //current_card.find("#btn-panda").attr('id','the_new_id');

                add_card(current_card)
            } /*loop on all offers*/
        } else {
            show_intro()
            show_dialog("No result found", "Panda Advisor")
        } /*make sure offers not null*/


    }
}

function show_intro() {
    $('.video-container').show();
    $('.intro-card').show();

    $('.card-columns').hide()
}

function hide_intro() {
    $('.video-container').hide();
    $('.intro-card').hide();

    $('.card-columns').show()
}

function add_card(current_card) {
    $(".card-columns").append(current_card)
}

function show_dialog(response, type) {

    $("#dialog-panda").find(".modal-title").html(type)
    $("#dialog-panda").find("#dialog-content").html(response)
    jQuery("#dialog-panda").modal('show');

    //alert(response)

}

/*static data*/