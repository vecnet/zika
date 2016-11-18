/**
 * This file contains the javascript necessary to render the d3 choropleth of Columbia
 * by municipality
 * Created on 11/16/16.
 */
		$(document).ready(function() {

            document.getElementById("date-dropdown").onchange = function() {

                window.alert(document.getElementById("date-dropdown").value);
            };

        });


// Function t
function dateSelected() {
    var select_value = document.getElementById("date-dropdown");
    var show_picked_date = document.getElementById("picked-date");
    show_picked_date.value = select_value.value;
}
