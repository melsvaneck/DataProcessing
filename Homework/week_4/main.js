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

  d3.select("body")
    .append("p")
    .text("This bar chart represents the amount of " + data + " species in the Netherlands");

  // open the json data
  d3.json("Data.json").then(function(species) {

    // make lists for the chosen data
    var values = [];
    var names = [];

    // fill lists for the chosen data for the scaling
    function getData(data) {
      for (var key in species) {
        values.push(species[key][data]);
        names.push(species[key].Common_name);
      };
      return values, names
    };

    getData(data);
    // get a max value of the chosen data for the scaling
    var maxValue = Math.max.apply(null, values);

    // round the max value to a round number in tens or 50s
    // according to the max value
    if (maxValue > 140) {
      var maxRounded = Math.ceil(maxValue / 50) * 50;
    } else {
      var maxRounded = Math.ceil(maxValue / 10) * 10;
    }

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

    // make same amount of bars as objects in the species array
    // colour the bars (tim approved)
    var bars = svg.selectAll("bar")
      .data(species)
      .enter()
      .append("rect")
      .attr("fill", function(d, i) {
        return color(i);
      });

    // Create yScale
    var yScale = d3.scaleLinear()
      .domain([d3.min(values), maxRounded])
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
    bars.attr("x", function(d, i) {
        return xScale(d.Common_name);
      })
      .attr("width", xScale.bandwidth())

      //  tooltip
      .on('mouseover', tip.show)
      .on('mouseout', tip.hide)

      // animation
      .attr("y", h - marginBottom)
      .transition()
      .duration(1000)
      .delay(function(d, i) {
        return i * 150;
      })

      // y values and height
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
