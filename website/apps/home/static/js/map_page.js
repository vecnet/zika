/*jslint browser:true*/
/*global window*/
/**
 * This file contains javascript functions for buttons, etc on the map page
 * Created on 11/30/16.
 */


/**
 * Function to change page based on left or right arrow button click from the simulation menu
 *
 * @param all_sim_with_model_list: List of all simulations that have the chosen model
 * @param current_sim_index: Index of the currently selected simulation
 * @param prev_or_next: Indicator whether the left (previous, or 0) button was clicked or the
 *        right (next, or 1) button was clicked
 */
function prevNextSimBtnClick(all_sim_with_model_list, current_sim_index, prev_or_next) {
    "use strict";
    var segments = window.location.pathname.toString().split("/");
    if (prev_or_next === 0) {
        if (current_sim_index !== 0) {
            segments[segments.length - 2] = all_sim_with_model_list[current_sim_index - 1].id;
        } else {
            window.alert("You are looking at the most recent simulation");
        }
    } else if (prev_or_next === 1) {
        if (current_sim_index !== (all_sim_with_model_list.length - 1)) {
            segments[segments.length - 2] = all_sim_with_model_list[current_sim_index + 1].id;
        } else {
            window.alert("You are looking at the oldest simulation");
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




