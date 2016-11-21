/**
 * This file contains the javascript necessary to render the d3 choropleth of Columbia
 * by municipality
 * Created on 11/16/16.
 */
$(document).ready(function() {

    //Width and height
    var w = 1000;
    var h = 600;

    //Define map projection
    var projection = d3.geo.albersUsa()
            .translate([0, -350])
            .scale([1000]);

    //Define path generator
    var path = d3.geo.path()
            .projection(projection);

    //Define quantize scale to sort data values into buckets of color
    var color = d3.scale.quantize()
            .range(["rgb(237,248,233)", "rgb(186,228,179)", "rgb(116,196,118)", "rgb(49,163,84)", "rgb(0,109,44)"]);
    //Colors taken from colorbrewer.js, included in the D3 download

    //Create SVG element
    var div = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);
    var svg = d3.select("body").select("svg");

    //Load in zika choropleth map data
    var csvpath = $("#csv-url").attr("data-url"); //"{{ generatefilepath }}";

    d3.csv(csvpath, function (data) {
        //Set input domain for color scale
        color.domain([
            d3.min(data, function (d) {
                return d.value;
            }),
            d3.max(data, function (d) {
                return d.value;
            })
        ]);

        //Load in GeoJSON data
        d3.json("/static/examples/colombia_admin3.json", function (json) {
            //Merge the ag. data and GeoJSON
            //Loop through once for each ag. data value
            for (var i = 0; i < data.length; i++) {
                //Grab state name
                var dataState = data[i].ID_ESPACIA;
                //Grab data value, and convert from string to float
                var dataValue = data[i].value;

                //Find the corresponding state inside the GeoJSON
                for (var j = 0; j < json.features.length; j++) {

                    var jsonState = json.features[j].properties.ID_ESPACIA;

                    if (dataState == jsonState) {
                        //Copy the data value into the JSON
                        json.features[j].properties.value = dataValue;
                        //Stop looking through the JSON
                        break;

                    }
                }
            }

            //Bind data and create one path per GeoJSON feature
            svg.selectAll("path")
                    .data(json.features)
                    .enter()
                    .append("path")
                    .attr("d", path)
                    .style("fill", function (d) {
                        //Get data value
                        var value = d.properties.value;
                        if (value) {
                            //If value exists…
                            return color(value);
                        } else {
                            //If value is undefined…
                            return "#ccc";
                        }
                    })
                    .on("click", function(d){
                        var simulationumber = "{{ sim_id }}";
                        var url = $("#url").attr("data-url");
                        url += simulationumber;
                        url += "/";
                        url += d.properties.ID_ESPACIA;
                        document.getElementById('iframe2').src = url;
                    })
                    .on("mouseover", function(d) {
                        d3.select(this).transition().duration(300).style("opacity", 1);
                        div.transition().duration(300)
                                .style("opacity", 1);
                        div.text(d.properties.NOM_DEPART + " " + d.properties.NOM_MUNICI + " " + d.properties.value)
                                .style("left", (d3.event.pageX) + "px")
                                .style("top", (d3.event.pageY -30) + "px");
                    })
                    .on("mouseout", function() {
                        d3.select(this)
                                .transition().duration(300)
                                .style("opacity", 0.8);
                        div.transition().duration(300)
                                .style("opacity", 0);
                    })
        });
    });
});

