/*jslint browser:true*/
/*global window*/
/**
 * This file contains javascript functions for buttons, etc on the map page
 * Created on 11/30/16.
 */


/**
 * Function to change page based on left or right arrow button click from the simulation menu
 * NOTE: all_sim_with_model_list is ORDERED from most recent to least recent. Thus, the most recent
 * simulation will have index 0 and the oldest simulation will have index length-1.
 *
 * @param all_sim_with_model_list: List of all simulations that have the chosen model
 * @param current_sim_index: Index of the currently selected simulation
 * @param prev_or_next: Indicator whether the left (previous, or 0) button was clicked or the
 *        right (next, or 1) button was clicked
 */
function prevNextSimBtnClick(all_sim_with_model_list, current_sim_index, prev_or_next) {
    "use strict";
    var segments = window.location.pathname.toString().split("/");
    // We only want to change the simulation id when the button is clicked.
    // if there are 6 segments, then no municipality code is included. If there are 7 segments
    // then the municipality code is in the url.
    var replace_index = null;
    if (segments.length === 6) {
        replace_index = segments.length - 2;
    } else if (segments.length === 7) {
        replace_index = segments.length - 3;
    }
    // the previous button was clicked, want to go back in time
    if (prev_or_next === 0) {
        // if the current simulation index is not the oldest in the list, increase index
        if (current_sim_index !== (all_sim_with_model_list.length - 1)) {
            segments[replace_index] = all_sim_with_model_list[current_sim_index + 1].id;
        } else {
            window.alert("You are looking at the oldest simulation");
        }
    } else if (prev_or_next === 1) {  // next button was clicked, want to go forward in time
        // if the current simulation index is not the most recent in the list, decrease index
        if (current_sim_index !== 0) {
            segments[replace_index] = all_sim_with_model_list[current_sim_index - 1].id;
        } else {
            window.alert("You are looking at the most recent simulation");
        }
    } else {
        window.alert("Error changing simulations. Please try again.");
    }
    window.location = segments.join("/");
}

// function prevNextDateBtnClick(new_date) {
//     "use strict";
//     // If we already have a date, we want to replace that date with the previous date in the list
//     if (window.location.pathname.match("(/(1|2)[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])/$)")){
//         var basePath = window.location.pathname.toString();
//         var segments = basePath.split("/");
//         segments[segments.length - 2] = "" + new_date;
//         var newUrl = segments.join("/");
//         window.location = newUrl;
//     }
//     // else {
//     //     window.location = prev + '/';
//     // }
// }




