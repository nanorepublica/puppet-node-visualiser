
// graph stuff with d3 :)

var diameter = 960;

var tree = d3.layout.tree()
    .size([360, diameter / 2 - 120])
    .separation(function(a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });

var diagonal = d3.svg.diagonal.radial()
    .projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });

var svg = d3.select("#graph").append("svg")
    .attr("width", diameter)
    .attr("height", diameter - 150)
  .append("g")
     .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")"); //may change this transform?
    //.attr("transform", "translate(" + 200 + "," + 20 + ")"); //may change this transform?

d3.json("/nodes", function(error, root) {
  var nodes = tree.nodes(root);
  nodes = _.map(nodes, function(node) {
    node.x = isNaN(node.x) ? 180 : node.x;
    return node;
  });
  var links = tree.links(nodes);

  var link = svg.selectAll(".link")
      .data(links)
    .enter().append("path")
      .attr("class", "link")
      .attr("d", diagonal);

  var node = svg.selectAll(".node")
      .data(nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })

  node.append("circle")
      .attr("r", 4.5)
      .on("mouseover", mouseover)
      .on("mousemove", mousemove)
      .on("mouseout", mouseout);

  node.append("text")
      .attr("dy", ".31em")
      .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
      .attr("transform", function(d) { return d.x < 180 ? "translate(8)" : "rotate(180)translate(-8)"; })
      .text(function(d) { return d.name; });

});

var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 1e-6);

function mouseover() {
  div.transition()
      .duration(500)
      .style("opacity", 0.7);
}

function mousemove(d) {
  div
    .style("left", (d3.event.pageX + 17) + "px")
    .style("top", (d3.event.pageY + 6) + "px");
  if (d.classes.length > 0) {
    div.text(d.classes)
  } else {
    div.text('No classes included on this node')
  }
}

function mouseout() {
  div.transition()
      .duration(500)
      .style("opacity", 1e-6);
}
