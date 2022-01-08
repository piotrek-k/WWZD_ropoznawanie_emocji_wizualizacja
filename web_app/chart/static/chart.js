//d3.json("/static/data.json", function(data) {
//        console.log(data);
//    });


// Commented version of
// https://bl.ocks.org/mbostock/3884955

// Variables
var svg = d3.select("svg"),
    margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = svg.attr("width") - margin.left - margin.right,
    height = svg.attr("height") - margin.top - margin.bottom;


// SVG G to provide D3 Margin Convention
g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Date Parser takes in Date string and returns JS Data Object
var parseTime = d3.timeParse("%Y%m%d");

// Scale X - time scale
// Scale Y - linear scale
// Scale Z - color categorical scale
var x = d3.scaleTime().range([0, width]),
    y = d3.scaleLinear().range([height, 0]),
    z = d3.scaleOrdinal(d3.schemeCategory10);

// D3 Line generator with curveBasis being the interpolator
var line = d3.line()
    .curve(d3.curveBasis)
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.temperature); });

// TSV AJAX call
// type function does the data pre-processing
d3.tsv("/static/data.tsv", type, function(error, data) {
  if (error) throw error;

  // Construct new data structure
  // array of arrays
  // 1st level of arrays are based on City
  //   - so 3 arrays at this level
  // 2nd level of arrays are based on date and temp for each city
  //   - so 366 arrays at this level per city
  var cities = data.columns.slice(1).map(function(id) {
    return {
      id: id,
      values: data.map(function(d) {
        return {date: d.date, temperature: d[id]};
      })
    };
  });

  // Using the initial data figure out the min / max dates
  x.domain(d3.extent(data, function(d) { return d.date; }));

  // Using the constructed cities data figure out the min / max temperatures
  // Note the nested d3.min's
  //   - for each city figure out the min temp
  //   - then figure out the min temp from the city's min temp
  // Note the nested d3.max's
  //   - for each city figure out the max temp
  //   - then figure out the max temp from the city's max temp
  y.domain([
    d3.min(cities, function(c) { return d3.min(c.values, function(d) { return d.temperature; }); }),
    d3.max(cities, function(c) { return d3.max(c.values, function(d) { return d.temperature; }); })
  ]);

  // Using the constructed cities data get the domain from the City id
  // We get ["New York", "San Francisco", "Austin"]
  z.domain(cities.map(function(c) { return c.id; }));

  // Create X Axis
  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  // Create Y Axis
  // Add Text label to Y axis
  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("fill", "#000")
      .text("Temperature, ºF");

  // Create a <g> element for each city
  // Note that 3 1st level arrays, so we get 3 g's
  var city = g.selectAll(".city")
    .data(cities)
    .enter().append("g")
      .attr("class", "city");

  // Create a <path> element inside of each city <g>
  // Use line generator function to convert 366 data points into SVG path string
  city.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return z(d.id); });

  // Append text to each city's <g>
  // Data join using function to access and create a new data structure based on inherited data structure
  // Note:
  //   - d.values[d.values.length gives us the last element of the 366 element array
  // This helps us to figure out how to correctly place city line text labels
  city.append("text")
      .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temperature) + ")"; })
      .attr("x", 3)
      .attr("dy", "0.35em")
      .style("font", "10px sans-serif")
      .text(function(d) { return d.id; });
});

// Function to process the data when it gets ingested by the AJAX call
function type(d, _, columns) {
  d.date = parseTime(d.date);
  for (var i = 1, n = columns.length, c; i < n; ++i) d[c = columns[i]] = +d[c];
  return d;
}
