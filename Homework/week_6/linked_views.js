// text
d3.select("head").append("title").text("BEES");
d3.select("body").append("h1").text("Mels van Eck");
d3.select("body").append("h1").text("12505757").style('top', '50px');
d3.select("body").append("text").text("Deze map laat zien oop welke locatie er bijen kolonies leven in Amsterdam," +
    " zowel wilde bijen als honingbijen zijn er te zien." +
    "klik op een buurt om de verhoudingen tussen honing en wilde bijen te zien," +
    "klik op de gekleurde puntjes op de kaart om te zien hoeveel kolonies honingbijen er leven op deze plek" +
    'of welke soorten er zijn waargenomen.')
  .attr("class", "text_box");

// text boxes
d3.select("body").append("text")
  .attr('class', 'info')
  .style("top", '110px')
  .style("font-size", "24px")
  .text('soorten of aantal kasten:')
  .attr("alignment-baseline", "middle");

d3.select("body").append("div")
  .attr('class', 'box')

// updateable textbox
info = d3.select("body").append("p")
  .attr('class', 'info');

// variables for the svg element
var margin = {
  top: 20,
  right: 20,
  bottom: 20,
  left: 20
};

var width = 1000
var height = 730

// make the svg
var svg = d3.select("body")
  .append("svg")
  .attr("width", width)
  .attr("height", height)
  .attr('class', 'map');

// placing of the geojson
var projection = d3.geoAlbers()
  .center([4.91, 52.346667])
  .parallels([51.5, 51.49])
  .rotate(120)
  .scale(250000)
  .translate([width / 2, height / 2]);

// make variable path
var path = d3.geoPath()
  .projection(projection);

// naming the city parts for coloring later on
var stadsdeel = {
  "A": "Centrum",
  "B": "Westpoort",
  "E": "West",
  "M": "Oost",
  "K": "Zuid",
  "F": "Nieuw west",
  "N": "Noord",
  "T": "Zuidoost"
}

// making the color scales
var colorScale = d3.scaleOrdinal(d3.schemeCategory20)
colorStadsdelen = d3.scaleOrdinal(d3.schemeCategory20); //d3.schemeGreys
colorLines = d3.scaleSequential(d3.schemeCategory20);

// make the div for the tooltip
var div = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

// load in all the data files
d3.queue()
  .defer(d3.json, "buurten.json")
  .defer(d3.json, "mokum.json")
  .defer(d3.csv, "wild_bees.csv")
  .defer(d3.csv, "honey_bees.csv")
  .await(ready);

// make the map
function ready(error, buurten, mokum, wild_bees, honey_bees) {

  // onchange function for dot selection on the map
  document.getElementById("myList").onchange = function() {
    scatterPoints(this.value)
  }

  if (error) throw error;

  // make data ready for usage
  var stadsdelen = topojson.feature(buurten, buurten.objects.buurten).features;
  var water = topojson.feature(mokum, mokum.objects.GEBIED_STADSDELEN).features;

  // make the undelying maap of amsterdam to simulate water
  svg.selectAll(".water")
    .data(water)
    .enter().insert("g")
    .append("path")
    .attr("class", "water")
    .attr("d", path)
    .attr("fill", function(d) {
      return "#7bd4e0";
    });

  // Draw the buurten
  svg.selectAll(".buurt")
    .data(stadsdelen)
    .enter().insert("g")
    .append("path")
    .attr("class", "buurt")
    .attr("d", path)
    .on("click", function(d) {
      redraw(makeData(inside(d.geometry.coordinates[0], honey_bees, wild_bees)), d.properties.Buurtcombinatie)
    })
    .on("mouseover", function(d) {
      div.transition()
        .duration(200)
        .style("opacity", .9);
      div.html(d.properties.Buurtcombinatie)
        .style("left", (d3.event.pageX) + "px")
        .style("top", (d3.event.pageY - 40) + "px");
    }).on("mouseout", function(d) {
      div.transition()
        .duration(500)
        .style("opacity", 0);
    })
    .attr("fill", function(d) {
      return colorStadsdelen(d.properties.Stadsdeel_code[0])
    })

  // Draw borders around buurten
  svg.append("path")
    .attr("class", "buurt-borders")
    .attr("d", path(topojson.mesh(buurten, buurten.objects.buurten, function(a, b) {
      return a !== b;
    })));

  // Draw borders around stadsdelen
  svg.append("path")
    .attr("class", "stadsdeel-borders")
    .attr("d", path(topojson.mesh(buurten, buurten.objects.buurten, function(a, b) {
      return stadsdeel[a.properties.Stadsdeel_code] !== stadsdeel[b.properties.Stadsdeel_code];
    })));

  // draw the first pie chart and make the first scatter of bee points
  redraw(makeData(inside(stadsdelen[0].geometry.coordinates[0], honey_bees, wild_bees)), stadsdelen[0].properties.Buurtcombinatie)
  scatterPoints("all")

  // this function scatters the points around the map according to the choice of the dropdown menu
  function scatterPoints(option) {
    // remove all the points
    svg.selectAll("circle").remove();

    // wild bee choice
    if (option == "all" || option == "wild") {
      // Draw the points for the wild bees
      var wildBees = svg.selectAll("wildBees")
        .data(wild_bees)
        .enter().append("circle")
        .attr("transform", "translate(" + projection([4.91, 52.346667]) + ")")
        .transition()
        .duration(1000)
        .attr("transform", function(d) {
          return "translate(" + projection([d["LNG"], d["LAT"]]) + ")";
        })
        .attr("class", "wildBees");
    };

    // honey bee choice
    if (option == "all" || option == "honey") {
      // Draw the points for the honeybees
      var honeyBees = svg.selectAll("honeyBees")
        .data(honey_bees)
        .enter().append("circle")
        .attr("transform", "translate(" + projection([4.91, 52.346667]) + ")")
        .transition()
        .duration(1000)
        .attr("transform", function(d) {
          return "translate(" + projection([d["LNG"], d["LAT"]]) + ")";
        })
        .attr("class", "honeyBees");
    };

    // onclickfunction to show parts of the data
    svg.selectAll("circle").on("click", function(d) {
      showInfo(d);
    });

  };
};

// margins for the piechart
var piemargin = {
    top: 100,
    bottom: 10,
    left: 10,
    right: 10
  },

  // sixes for the pie chart
  piewidth = 500,
  pieheight = 700,
  radius = Math.min(piewidth, pieheight) / 2;

// make the svg for the pie chart
var piesvg = d3.select("body")
  .append("svg")
  .attr('class', "pie")
  .attr("width", piewidth + piemargin.left + piemargin.right)
  .attr("height", pieheight + piemargin.top + piemargin.bottom)
  .append("g")
  .attr("transform", "translate(" + ((piewidth / 2) + piemargin.left) + "," + ((pieheight / 2) + piemargin.top) + ")");

// make scale for coloring of the pie chart
var color = d3.scaleOrdinal(['#f1f442', '#ffb310'])

// make pie variable
var pie = d3.pie()
  .sort(null)
  .value(function(d) {
    return d.value;
  });

var arc = d3.arc()
  .outerRadius(radius)
  .innerRadius(0);

// make all the texts for the legend of the pie chart
piesvg.append("text").attr("x", -230).attr("y", -420).text("Buurt:").attr("class", "honeyLegend").attr("alignment-baseline", "middle")
piesvg.append("circle").attr("cx", -220).attr("cy", -370).attr("class", "honeyLegend")
piesvg.append("text").attr("x", -190).attr("y", -370).text("Honing bijen kolonies").attr("class", "honeyLegend").attr("alignment-baseline", "middle")
piesvg.append("circle").attr("cx", -220).attr("cy", -315).attr("class", "wildLegend")
piesvg.append("text").attr("x", -190).attr("y", -315).text("Waargenomen bijen soorten").attr("class", "wildLegend").attr("alignment-baseline", "middle")

// make updateable textboxes for the pie chart
text = piesvg.append("text")
  .attr("x", -160)
  .attr("y", -412.5)
  .attr("class", "honeyLegend");

honeyAmount = piesvg.append("text")
  .attr("x", 110)
  .attr("y", -362.5)
  .attr("class", "honeyLegend");

wildAmount = piesvg.append("text")
  .attr("x", 110)
  .attr("y", -310)
  .attr("class", "honeyLegend");



// this function checks what points are inside the selected area
function inside(polygon, honey_bees, wild_bees) {

  // make sure to pick the right polygon
  if (polygon[0].length > 2) {
    polygon = polygon[0];
  }

  var honeyBees = []
  // this part checks wich points are in the area
  Object.values(honey_bees).forEach(value => {
    var x = value.LNG,
      y = value.LAT;
    var inside = false;
    for (var i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
      var xi = polygon[i][0],
        yi = polygon[i][1];
      var xj = polygon[j][0],
        yj = polygon[j][1];

      var intersect = ((yi > y) != (yj > y)) &&
        (x < (xj - xi) * (y - yi) / (yj - yi) + xi);

      if (intersect) inside = !inside;
    }
    if (inside == true) {
      honeyBees.push(value)
    };
  });

  var wildBees = []

  //  also for the wild bees
  Object.values(wild_bees).forEach(value => {
    var x = value.LNG,
      y = value.LAT;

    var inside = false;

    for (var i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
      var xi = polygon[i][0],
        yi = polygon[i][1];

      var xj = polygon[j][0],
        yj = polygon[j][1];

      var intersect = ((yi > y) != (yj > y)) &&
        (x < (xj - xi) * (y - yi) / (yj - yi) + xi);

      if (intersect) inside = !inside;
    }
    if (inside == true) {
      wildBees.push(value)
    };
  });

  return [honeyBees, wildBees];
};

// this function makes an an array of objects for the data in the selected area
function makeData(data, buurtnaam) {

  // count the amount of hives per area
  hives = 0
  data[0].forEach(function(item) {
    var x = parseInt(item.Aantal_kasten, 10);
    hives += x

  });

  // make an array of all the species (excluding duplicates)
  species = []
  data[1].forEach(function(item) {
    var array = item.Waargenomen_bijen.split("-");
    species = merge_array(species, array)
  });

  // make the array objects
  data = [{
    "name": "honeyBees",
    value: hives
  }, {
    "name": "wildBees",
    value: species.length
  }];

  return data;
};

// merge 2 arrays, skipping duplicates
function merge_array(array1, array2) {
  var result_array = [];
  var arr = array1.concat(array2);
  var len = arr.length;
  var assoc = {};

  while (len--) {
    var item = arr[len];

    if (!assoc[item]) {
      result_array.unshift(item);
      assoc[item] = true;
    }
  }
  return result_array;
};

// this function shows parts of selected data (dots)
function showInfo(d) {
  // check if wild bees or honey bees
  if (d.Waargenomen_bijen != undefined) {
    info.text(d.Waargenomen_bijen);
  } else {
    info.text(d.Aantal_kasten)
  }
}

// update pie chart
function redraw(data, buurtnaam) {
  text.text(buurtnaam)

  honeyAmount.data(data)
    .text(data[0].value)

  wildAmount.data(data)
    .text(data[1].value)

  // join
  var arcs = piesvg.selectAll(".arc")
    .data(pie(data), function(d) {
      return d.data.name;
    });

  // update
  arcs
    .transition()
    .duration(1500)
    .attrTween("d", arcTween);

  // enter
  arcs.enter().append("path")
    .attr("class", "arc")
    .attr("fill", function(d, i) {
      return color(i);
    })
    .attr("d", arc)
    .each(function(d) {
      this._current = d;
    });

}

// Store the displayed angles in _current.
// Then, interpolate from _current to the new angles.
// During the transition, _current is updated in-place by d3.interpolate.
function arcTween(a) {
  var i = d3.interpolate(this._current, a);
  this._current = i(0);
  return function(t) {
    return arc(i(t));
  };
}
