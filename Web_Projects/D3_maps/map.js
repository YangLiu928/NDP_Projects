var mapSource = "./us.json",
    dataSource = "./test-map.csv",
    dataType = "decPercent",
    colorType = "continuous"; //Set which type of data this map uses from the options in dataFormat

var width = 960*.8,
    height = 720*.8;


// Define increments for data scale
var dataScale = [],
    min = .0025, //Floor for the first step
    max = .035, //Anything above the max is the final step
    steps = 3,
    increment = (max-min)/(steps-1);
// Create the scale of data values from min to max by # of steps
for (var step = 0; step < steps; step++) {
    dataScale.push(min + increment * step);
}

// Create distinct colors for each increment based on two base colors
var colors = [],
    borderColor = "#fff", //Color of borders between states
    noDataColor = "#ccc", //Color applied when no data matches an element
    lowBaseColor = "#fea455", //Color applied at the end of the scale with the lowest values
    highBaseColor = "#450151"; //Color applied at the end of the scale with the highest values

var colorTypes = {
    // For color scale with separated groups
    grouped: d3.scale.linear()
        .domain([0,steps-1])
        .range([lowBaseColor,highBaseColor])
        .interpolate(d3.interpolateHcl),
        //Don't like the colors you get? Try interpolateHcl or interpolateHsl!

    // For continuous color scale
    continuous: d3.scale.linear()
        .domain([min, max])
        .range([lowBaseColor,highBaseColor])
        .interpolate(d3.interpolateHcl)
        //Don't like the colors you get? Try interpolateHcl or interpolateHsl!
};

// Create basic legend and add generated colors to the 'colors' array
// Should replace this with D3.js Axis
for (var c = 0; c < steps; c++) {
    colors.push(colorTypes.grouped(c));
}

var svg = d3.select("#map-container").append("svg")
    .attr("width", width)
    .attr("height", height);

var tooltip = d3.select("#map-container").append("div")
    .attr("class", "tooltip")
    .style("position", "absolute")
    .style("opacity", 0),
    dataFormat = {
        intPercent: d3.format("%"),
        decPercent: d3.format(".1%")
    };

var projection = d3.geo.albersUsa()
    .scale(width*(width/height))
    .translate([width / 2, height - height * 0.6]);

var path = d3.geo.path()
    .projection(projection);

var mapColor;

if (colorType == "grouped") {
    mapColor = d3.scale.quantize()
        .domain([min, max])
        .range(colors);
} else if (colorType == "continuous") {
    mapColor = colorTypes.continuous;
}

var map = svg.append("g")
    .attr("class", "states");

var labels = svg.append("g")
    .attr("class", "labels");

var legend = svg.append("g")
    .attr("class", "legend")
    .attr("transform", "translate(0," + (height - height * 0.1) + ")");

var labelOffsets = { //To preserve position with changes to width and height, set all values to percentage * width or height
    2: {
        x: 105,
        y: 490
    },
    9: {
        x: 910,
        y: 310,
        small: true
    },
    10: {
        x: 910,
        y: 390,
        small: true
    },
    11: {
        x: 910,
        y: 470,
        small: true
    },
    12: {
        x: 775,
        y: 500
    },
    13: {
        x: 725,
        y: 405
    },
    15: {
        x: 275,
        y: 560
    },
    22: {
        x: 555,
        y: 465
    },
    23: {
        x: 905,
        y: 70
    },
    24: {
        x: 910,
        y: 430,
        small: true
    },
    25: {
        x: 910,
        y: 230,
        small: true
    },
    26: {
        x: 670,
        y: 170
    },
    33: {
        x: 805,
        y: 50,
        small: true
    },
    34: {
        x: 910,
        y: 350,
        small: true
    },
    36: {
        x: 825,
        y: 155
    },
    37: {
        x: 800,
        y: 330
    },
    44: {
        x: 910,
        y: 270,
        small: true
    },
    45: {
        x: 770,
        y: 375
    },
    50: {
        x: 725,
        y: 50,
        small: true
    },
    51: {
        x: 800,
        y: 280
    },
    54: {
        x: 750,
        y: 270
    },
    55: {
        x: 590,
        y: 155
    }
};

var smallStateRects = [
    {
        id: 9
    },
    {
        id: 10
    },
    {
        id: 11
    },
    {
        id: 24
    },
    {
        id: 25
    },
    {
        id: 33
    },
    {
        id: 34
    },
    {
        id: 44
    },
    {
        id: 50
    }
];

queue()
    .defer(d3.json, mapSource)
    .defer(d3.csv, dataSource)
    .await(ready);

function ready(error, us, data) {
    if (error) return console.error(error);

    //add states
    map.selectAll("path")
        .data(topojson.feature(us, us.objects.states).features)
    .enter().append("path")
        .attr("d", path)
        .attr("fill", noDataColor)
        .attr("class", function(d){return "state" + d.id;});

    //add small state rectangles for legend
    map.selectAll("rect")
        .data(smallStateRects)
    .enter().append("rect")
        .attr("width", function(){return scaleOffset(28, "width");})
        .attr("height", function(){return scaleOffset(28, "height");})
        .attr("x", function(d) {
            return scaleOffset((labelOffsets[d.id].x + 10), "width");
        })
        .attr("y", function(d) {
            return scaleOffset((labelOffsets[d.id].y - 12), "height");
        })
        .attr("fill", noDataColor)
        .attr("class", function(d){return "state" + d.id;});

    //create group for labels
    var labelGroups = labels.selectAll("text")
        .data(topojson.feature(us, us.objects.states).features)
        .enter().append("g");

    labelGroups
        .append("text")
        .attr("class", "state-name")
        .attr("id", function(d){return "statename" + d.id;})
        .attr("text-anchor", function(d){
            if (labelOffsets[d.id] && labelOffsets[d.id].small === true) {
                return "end";
            } else {
                return "middle";
            }
        })
        .attr("transform", function(d){
            if (labelOffsets[d.id]) {
                return "translate(" + scaleOffset(labelOffsets[d.id].x, "width")
                + ","
                + scaleOffset(labelOffsets[d.id].y, "height") + ")";
            } else {
                var centroid = path.centroid(d),
                    x = centroid[0],
                    y = centroid[1];
                return "translate(" + (x) + "," + (y) + ")";
            }
        });

    labelGroups
        .append("text")
        .attr("class", "state-value")
        .attr("id", function(d){return "stateval" + d.id;})
        .attr("text-anchor", function(d){
            if (labelOffsets[d.id] && labelOffsets[d.id].small === true) {
                return "end";
            } else {
                return "middle";
            }
        })
        .attr("transform", function(d){
            if (labelOffsets[d.id]) {
                return "translate(" + scaleOffset(labelOffsets[d.id].x, "width")
                + ","
                + scaleOffset(labelOffsets[d.id].y + 14, "height") + ")";
            } else {
                var centroid = path.centroid(d),
                    x = centroid[0],
                    y = centroid[1];
                return "translate(" + (x) + "," + (y + 14) + ")";
            }
        });

    data.forEach(function(d){
        d3.selectAll(".state" + d.id)
            .style("fill", function(){ if (d.rate) { return mapColor(parseFloat(d.rate)); } })
            .on("mouseover", function(){ return addTooltip(d.state, d.rate); })
            .on("mousemove", function(){
                tooltip
                    .style("left", (d3.event.pageX - adjustment(d3.event.pageX)) + "px")
                    .style("top", (d3.event.pageY + 50) + "px");
            })
            .on("mouseout", function(d){ tooltip.transition().duration(200).style("opacity",0); });
        d3.select("#stateval" + d.id)
            .html(dataFormat[dataType](d.rate))
            .on("mouseover", function(){ return addTooltip(d.state, d.rate); })
            .on("mousemove", function(){
                tooltip
                    .style("left", (d3.event.pageX - adjustment(d3.event.pageX)) + "px")
                    .style("top", (d3.event.pageY + 50) + "px");
            })
            .on("mouseout", function(d){ tooltip.transition().duration(200).style("opacity",0); });
        d3.select("#statename" + d.id)
            .html(d.abbr)
            .on("mouseover", function(){ return addTooltip(d.state, d.rate); })
            .on("mousemove", function(){
                tooltip
                    .style("left", (d3.event.pageX - adjustment(d3.event.pageX)) + "px")
                    .style("top", (d3.event.pageY + 50) + "px");
            })
            .on("mouseout", function(d){ tooltip.transition().duration(200).style("opacity",0); });
    });

    map.append("path")
        .datum(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; }))
        .attr("fill", "none")
        .attr("stroke", "#fff")
        .attr("stroke-width", 1.5)
        .attr("stroke-linejoin", "bevel")
        .attr("d", path);

    drawLegend();
}

var adjustment = d3.scale.linear()
                .domain([0, width])
                .range([0, 100]);

function addTooltip(label, number) {
    tooltip.transition()
        .duration(200)
        .style("opacity", 1);

    tooltip
        .html(label + ": " + dataFormat[dataType](parseFloat(number)))
        .style("left", (d3.event.pageX - adjustment(d3.event.pageX)) + "px")
        .style("top", (d3.event.pageY + 50) + "px");
}

function drawLegend() {
    var legendData = [{"color": noDataColor, "label": "No Data"}],
        legendDomain = [],
        legendScale,
        legendAxis;

    for (var i = 0, j = colors.length; i < j; i++){
        var fill = colors[i];
        var label = dataFormat[dataType](min + increment*i) + ((i === j - 1) ? "+" : "-" + dataFormat[dataType](min + increment*(i+1)));
        legendData[i+1]= {"color": fill, "label": label};
    }

    for (var k = 0, x = legendData.length; k < x; k++){
        legendDomain.push(legendData[k].label);
    }

    legendScale = d3.scale.ordinal()
        .rangeRoundBands([0,width], 0.2)
        .domain(legendDomain);

    legendAxis = d3.svg.axis()
        .scale(legendScale)
        .orient("bottom");

    legend.call(legendAxis);

    legend.selectAll("rect")
        .data(legendData)
    .enter()
        .append("rect")
        .attr("x", function(d){return legendScale(d.label);})
        .attr("y", -30)
        .attr("height", 30)
        .attr("class", "legend-item")
        .transition()
        .duration(700)
        .attrTween("width", function(){return d3.interpolate(0,legendScale.rangeBand());})
        .attrTween("fill", function(d){return d3.interpolate("#fff",d.color);});
}

function scaleOffset(offset, type) {
    switch(type) {
        case "width":
            return (offset/960)*width;
        case "height":
            return (offset/720)*height;
    }
}