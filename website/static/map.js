/**
 * This file contains the javascript necessary to render the d3 choropleth of Columbia
 * by municipality
 * Created on 11/16/16.
 */
		$(document).ready(function() {

            // document.getElementById("date-dropdown").onchange = function() {
            //     window.alert(document.getElementById("picked-date").value);
            //     document.getElementById("picked-date").value = document.getElementById("date-d;ropdown").value
            //     // dateSelected();
            //     // window.alert(document.getElementById("date-dropdown").value);
            // };

        });


// Function t
function dateSelected() {
    // window.alert(select_value);
    var select_value = document.getElementById("date-dropdown").value;
    // window.alert(select_value);
    // var show_picked_date = document.getElementById("picked-date");
    document.getElementById("picked-date").value = select_value;
}
