/*
Name:mels van eck
Student number:12505757
This script Makes a bar chart out of data about threatened species in the Netherlands
*/

d3.select("head").append("title").text("Nice barchart!");
d3.select("body").append("h1").text("Mels van Eck");
d3.select("body").append("h1").text("12505757");


document.getElementById("myList").onchange = function() {
  makeBars(this.value)
}

function makeBars(data) {

  //remove previous charts if any
  d3.selectAll("svg").remove();
  d3.selectAll("p").remove();

  // make a modular text for each bar chart
  d3.select("body")
    .append("p")
    .text("This bar chart represents the amount of " + data + " species in the Netherlands");

  // open the json data
  d3.json("Data.json").then(function(species) {

    //Width, height and margins
    var w = 750;
    var h = 450;
    var marginLeft = 60;
    var marginRight = 50;
    var marginBottom = 150;
    var margintop = 25;
    var color = d3.scale.category20();

    // make the svg
    var svg = d3.select("body")
      .append("svg")
      .attr("height", h)
      .attr("width", w);

    svg.append("text")
      .attr("x", -300)
      .attr("y", 25)
      .attr("dy", ".25em")
      .attr("transform", "rotate(-90)")
      .text("Amount of " + data + " species");

    svg.append("text")
      .attr("x", 400)
      .attr("y", 10)
      .attr("dy", ".25em")
      .text(data + " species in the Netherlands");

    // make same amount of bars as objects in the species array
    // colour the bars (tim approved)
    var bars = svg.selectAll("bar")
      .data(species)
      .enter()
      .append("rect")
      .attr("fill", function(d, i) {
        return color(i);
      });

    // get a max value of the chosen data for the scaling for scaleLinear function
    var maxValue = d3.max(species, function(d) {
      return +d[data];
    });

    // round the max value to a round number in tens or 50s
    // according to the max value
    if (maxValue > 140) {
      var maxRounded = Math.ceil(maxValue / 50) * 50;
    } else {
      var maxRounded = Math.ceil(maxValue / 10) * 10;
    }

    // make an array of the common names for the scaleband function
    var names = species.map(obj => {
      return obj.Common_name;
    })

    // Create yScale
    var yScale = d3.scaleLinear()
      .domain([0, maxRounded])
      .range([h - marginBottom, margintop]);

    // Create xScale
    var xScale = d3.scaleBand()
      .domain(names)
      .paddingInner(0.05)
      .range([marginLeft, w - marginRight]);

    // make the y axis
    var yAxis = d3.axisLeft()
      .scale(yScale);

    // make the x axis
    var xAxis = d3.axisBottom()
      .scale(xScale)

    // make the tooltip
    const tip = d3.tip().html(d => d[data]);

    // call the tooltip
    svg.call(tip);

    //Append group and insert the y axis
    svg.append("g")
      .attr("transform", "translate(" + marginLeft + ", 0)")
      .call(yAxis)

    // x placing of the x axis
    var xAxisTranslate = h - marginBottom;

    // append group and insert the x-axis,rotate the names
    svg.append("g")
      .attr("transform", "translate(0, " + xAxisTranslate + ")")
      .call(xAxis)
      .selectAll("text")
      .attr("y", 0)
      .attr("x", 9)
      .attr("dy", ".35em")
      .attr("transform", "rotate(60)")
      .style("text-anchor", "start");

    //function for making the bars
    // x values and width first
    //hover and animation
    //y values and height last
    bars.attr("x", function(d, i) {
        return xScale(d.Common_name);
      })
      .attr("width", xScale.bandwidth())
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide)
      .attr("y", h - marginBottom)
      .transition()
      .duration(1000)
      .delay(function(d, i) {
        return i * 150;
      })
      .attr("y", function(d) {
        return yScale(d[data]);
      })
      .attr("height", function(d) {
        return h - yScale(d[data]) - marginBottom;
      })
  });
};

// make the bar chart for the first time
makeBars("Total");
