/**
 * This file contains the javascript functions for the date changing buttons
 * Created on 11/30/16.
 */

function prevNextDateBtnClick(new_date) {
    // If we already have a date, we want to replace that date with the previous date in the list
    if(window.location.pathname.match('(/(1|2)[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])/$)')){
        var basePath = window.location.pathname.toString();
        var segments = basePath.split('/');
        segments[segments.length - 2] = "" + new_date;
        var newUrl = segments.join("/");
        window.location = newUrl;
    } else {
        window.location = prev + '/';
    }
}
