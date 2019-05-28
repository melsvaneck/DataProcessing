window.onload = function() {

  d3.select("head").append("title").text("Scatter :)");
  d3.select("body").append("h2").text("Mels van Eck");
  d3.select("body").append("h2").text("12505757");
  // make a title for the chart
  d3.select("body")
    .append("p")
    .text("This scatterplot shows the teen pregnancy rate plotted \
     against teen violence rates");

  var teensInViolentArea = "https://stats.oecd.org/SDMX-JSON/data/CWB/AUS+AUT+BEL+BEL-VLG+CAN+CHL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+OAVG+NMEC+BRA+BGR+CHN+COL+CRI+HRV+CYP+IND+IDN+MLT+PER+ROU+RUS+ZAF.CWB11/all?startTime=2010&endTime=2017"
  var teenPregnancies = "https://stats.oecd.org/SDMX-JSON/data/CWB/AUS+AUT+BEL+BEL-VLG+CAN+CHL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+OAVG+NMEC+BRA+BGR+CHN+COL+CRI+HRV+CYP+IND+IDN+MLT+PER+ROU+RUS+ZAF.CWB46/all?startTime=1960&endTime=2017"
  var GDP = "https://stats.oecd.org/SDMX-JSON/data/SNA_TABLE1/AUS+AUT+BEL+CAN+CHL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+EU28+EU15+OECDE+OECD+OTF+NMEC+ARG+BRA+BGR+CHN+COL+CRI+HRV+CYP+IND+IDN+MLT+ROU+RUS+SAU+ZAF+FRME+DEW.B1_GE.HCPC/all?startTime=2010&endTime=2018&dimensionAtObservation=allDimensions"

  var requests = [d3.json(teensInViolentArea), d3.json(teenPregnancies), d3.json(GDP)];

  Promise.all(requests).then(function(response) {

    //  prepare the data for the plot
    dataSet = makeData()
    data = dataSet[0][2010];

    //Width,colors, height and margins
    var w = 900;
    var h = 500;
    legend = {
      width: 150,
      margin: 125,
      height: 300
    };
    margin = {
      left: 50,
      right: 50,
      bottom: 60,
      top: 25
    };
    var colors = ['#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd'];

    // create color scale
    var colorScale = d3.scaleLinear()
      .domain(linspace(d3.min(data, function(d) {
        return d.gdp; // input domain
      }), d3.max(data, function(d) {
        return d.gdp; // input domain
      }), colors.length))
      .range(colors);

    // create legendscale for yaxis
    var legendScale = d3.scaleLinear()
      .domain([0, d3.max(data, function(d) {
        return d.gdp; // input domain
      })])
      .range([legend.height, 0]);

    // Create yScale
    var yScale = d3.scaleLinear()
      .domain([0, d3.max(data, function(d) {
        return d.pregnancies; // input domain
      })])
      .range([h - margin.bottom, margin.top]);

    // Create xScale
    var xScale = d3.scaleLinear()
      .domain([0, d3.max(data, function(d) {
        return d.violence; // input domain
      })])
      .range([margin.left, w - margin.right]);

    // create axis for the legend
    var legendAxis = d3.axisRight()
      .scale(legendScale)
      .ticks(10)
      .tickFormat(d3.format("$.2f"));

    // make the y axis
    var yAxis = d3.axisLeft()
      .scale(yScale);

    // make the x axis
    var xAxis = d3.axisBottom()
      .scale(xScale)

    // make the svg
    var svg = d3.select("body")
      .append("svg")
      .attr("height", h)
      .attr("width", w);

    // make the svg for the legend
    var legendSvg = d3.select('body')
      .append('svg')
      .attr('width', legend.width)
      .attr('height', h)

      svg.append("rect")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("fill", "#686868");

    // add texts to axes of the plot
    svg.append("text")
      .attr("x", -400)
      .attr("y", 15)
      .attr("dy", ".25em")
      .attr("transform", "rotate(-90)")
      .text("Teen pregnancy rate (%)")
      .attr("fill", "white");

    svg.append("text")
      .attr("x", 100)
      .attr("y", h - 25)
      .attr("dy", ".25em")
      .text("Children (0-17) living in areas with problems with crime or violence (%)")
      .attr("fill", "white");

    // make the scattered circles
    var circle = svg.selectAll("circle")
      .data(data)
      .enter()
      .append("circle")
      .attr("fill", function(d) {
        return colorScale(d.gdp)
      })
      .attr("cx", function(d) {
        return xScale(d.violence);
      })
      .attr("cy", function(d) {
        return yScale(d.pregnancies);
      })
      .attr("r", 10)
      .on("mouseover", function(d) {
        div.transition()
          .duration(200)
          .style("opacity", .9);
        div.html(d.country + "\n" + "$" + Math.round(d.gdp))
          .style("left", (d3.event.pageX) + "px")
          .style("top", (d3.event.pageY - 40) + "px");
      })
      .on("mouseout", function(d) {
        div.transition()
          .duration(500)
          .style("opacity", 0);
      });

    // Define the div for the tooltip
    var div = d3.select("body").append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);

    // insert y axis
    svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + margin.left + ", 0)")
      .call(yAxis)

    // append group and insert the x-axis
    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0, " + (h - margin.bottom) + ")")
      .call(xAxis)

    // call functions to make the sliderbar and the legend
    years = dataSet[1];
    makeSlider(years);
    makeLegend()

    function makeLegend() {
      // make text for the legend

      legendSvg.append("rect")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("fill", "#686868");

      legendSvg.append("text")
        .attr("x", 0)
        .attr("y", 80)
        .attr("dy", ".25em")
        .text("GDP in Dollars")
        .attr("fill","white");

      // make the bar gradient
      var gradient = legendSvg.append('defs')
        .append('linearGradient')
        .attr('id', 'gradient')
        .attr('x1', '0%')
        .attr('y1', '100%')
        .attr('x2', '0%')
        .attr('y2', '0%')
        .attr('spreadMethod', 'pad');



      // insert the legend axis
      legendSvg.append("g")
        .attr("class", "z axis")
        .attr("transform", "translate(" + (legend.width - legend.margin) + ", 100)")
        .call(legendAxis);

      // make the colorScaling grdient
      var pct = linspace(0, 100, colors.length).map(function(d) {
        return Math.round(d) + '%';
      });

      var colourPct = d3.zip(pct, colors);

      colourPct.forEach(function(d) {
        gradient.append('stop')
          .attr('offset', d[0])
          .attr('stop-color', d[1])
          .attr('stop-opacity', 1);
      });

      // make the coloured rectangle
      legendSvg.append('rect')
        .attr('x', 0)
        .attr('y', 100)
        .attr('width', legend.width - legend.margin)
        .attr('height', legend.height)
        .style('fill', 'url(#gradient)');

    }

    function makeSlider(years) {
      // make the step slider per year, do the updateplot function on a change
      var sliderStep = d3
        .sliderBottom()
        .min(d3.min(years))
        .max(d3.max(years))
        .width(300)
        .tickFormat(d3.format('1'))
        .ticks(5)
        .step(1)
        .default(1)
        .on('onchange', val => {
          d3.select('p#value-step').text(d3.format('1')(val));
          updatePlot(dataSet[0][val]);
        });

      var gStep = d3
        .select('div#slider-step')
        .append('svg')
        .attr('width', 500)
        .attr('height', 100)
        .append('g')
        .attr("class", "slider")
        .attr('transform', 'translate(30,30)');

      gStep.call(sliderStep);

      d3.select('p#value-step').text(d3.format('1')(sliderStep.value()));

    }

    function updatePlot(data) {
      // update all the scales
      xScale.domain([0, d3.max(data, function(d) {
        return d.violence;
      })]);

      yScale.domain([0, d3.max(data, function(d) {
        return d.pregnancies;
      })]);

      colorScale.domain(linspace(d3.min(data, function(d) {
        return d.gdp;
      }), d3.max(data, function(d) {
        return d.gdp;
      }), colors.length));

      legendScale.domain([0, d3.max(data, function(d) {
        return d.gdp; // input domain
      })])

      // update the dots
      svg.selectAll("circle")
        .data(data)
        .transition()
        .duration(1000)
        .attr("fill", function(d) {
          return colorScale(d.gdp)
        })
        .attr("cx", function(d) {
          return xScale(d.violence);
        })
        .attr("cy", function(d) {
          return yScale(d.pregnancies);
        })
        .attr("r", 10);

      // update the x axis
      svg.select(".x.axis")
        .transition()
        .duration(100)
        .call(xAxis);

      // Update Y Axis
      svg.select(".y.axis")
        .transition()
        .duration(100)
        .call(yAxis);

      // update the legend axis
      legendSvg.select(".z.axis")
        .transition()
        .duration(100)
        .call(legendAxis);

    }

    function makeData(data) {

      // make different objects from the datasets
      var violent = transformResponse(response[0]);
      var pregnancies = transformResponse(response[1]);
      var money = transformResponsegdp(response[2]);

      // make a new array for all the data
      var allData = [];

      // loop through the keys (countries) of the violent teens data
      // get the data of the other sets with the same country name (if any)
      // loop through the values of these countries
      Object.keys(violent).forEach(key => {
        preg = pregnancies[key];
        gdp = money[key];
        Object.values(violent[key]).forEach(value => {

          // if there is data of pregnancies on the same country:
          if (preg) {

            // make array of corresponding data for the same year and country (if any)
            var found = preg.filter(d =>
              d.Time == value.Time && d.Country == value.Country
            );

            // if there is corresponding data :
            if (found.length > 0) {
              var data = {}
              data["country"] = value.Country
              data["year"] = value.Time
              data["pregnancies"] = found[0].Datapoint
              data["violence"] = value.Datapoint
            }

            // do the same for gdp
            if (gdp) {
              var found = gdp.filter(d =>
                d.Year == value.Time && d.Country == value.Country
              );
              if (found.length > 0) {
                data["gdp"] = found[0].Datapoint
              }
            }
            // push the object into an array
            allData.push(data)
          }
        })
      })

      // make an array of all the available years
      const temp = new Set(allData.map(d => d.year))
      var years = Array.from(temp);

      // make an object for the data
      dataSet = {};

      // put the data with corresponding years in the same array
      for (var i = 0; i < years.length; i++) {
        dataSet[years[i]] = get_data(allData, years[i]);
      }
      return [dataSet, years];
    }
  }).catch(function(e) {
    throw (e);
  });
};

// this function makes proper color domain
function linspace(start, end, n) {
  var out = [];
  var delta = (end - start) / (n - 1);
  var i = 0;
  while (i < (n - 1)) {
    out.push(start + (i * delta));
    i++;
  }
  out.push(end);
  return out;
}

// this function returns an array of all the available years (no doubles)
function get_data(allData, year) {
  var select = []
  Object.values(allData).forEach(values => {
    if (values.year == year) {
      select.push(values)
    }
  });
  return select
}
