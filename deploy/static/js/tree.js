var data = document.getElementById("data").innerHTML;

var table = d3.csvParse(data, function(d,i){
    return{
	id: d.Course,
	parentId: d.Prereq  };
});

//console.log(table);

var treeData = d3.stratify()(table);

var margin = {top: 20, right: 120, bottom: 20, left: 120},
 width = 1920 - margin.right - margin.left,
 height = 1080 - margin.top - margin.bottom;
 
var i = 0;
var currdepth = 1;
var tree = d3.layout.tree()
    .size([height, width]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

root = treeData;

update(root,1);
function update(source,depth) {
    for(i = 1; i<= depth; i++){
	svg.append("circle").attr('class','buttons').attr('r',10).attr('x', 180).attr('y', 10).attr('selected',false).style("fill","green").attr('transform', 'translate(' + (i * 180) + ",0)");
    };
  var nodes = tree.nodes(root).reverse(),
   links = tree.links(nodes);

  // Normalize for fixed-depth.
    nodes.forEach(function(d) { d.y = d.depth * 180; });
    //nodes.forEach(function(d){console.log(d.depth <= depth); if(d.depth <= depth){console.log("depth is good"); d._children = false}else{d._children = d.children; d.children = null;};});

  // Declare the nodesâ€¦
    var node = svg.selectAll("g.node")
	.data(nodes, function(d) { return d.id || (d.id = ++i); });
    var updatecolor = function(){
	d3.selectAll('rect').transition().duration(300).style("fill",function(d){return d.selected?"green":"#fff";});
    };
	    // Enter the nodes.
  var nodeEnter = node.enter().append("g")
      .attr("class", "node")
    .attr("display", function(d){return d.depth > depth?'none':''})
      .on('click', function(d){d.selected = d.selected?false:true; updatecolor() } ) 
      .attr("transform", function(d) { 
	  return "translate(" + d.y + "," + d.x + ")"; });

  nodeEnter.append("rect")
	.attr("width", function(d){ return d.id.split('').length * 6;})
	.attr("height", 20).attr("y",-10)
	.attr("display",function(d){d.depth <= depth?'none':'unset'})
	.style("fill",function(d){return d.selected?"green":"#fff";})
	.style("stroke-width","1")
	.style("stroke","rgb(0,0,0)");
    //untested
	//.on('click', function(d){
	  //  d3.select(d).style("fill", "green")}
	   //);

  nodeEnter.append("text")
   .attr("x", function(d) { 
    return 0 })
   .attr("dy", ".35em")
   .attr("text-anchor", function(d) { 
    return "start"; })
   .text(function(d) { return d.id; })
   .style("fill-opacity", 1).style('font-size','10px');

  // Declare the linksâ€¦
  var link = svg.selectAll("path.link")
   .data(links, function(d) { return d.target.id; });

  // Enter the links.
  link.enter().insert("path", "g")
   .attr("class", "link")
    .attr("display",function(d){return d.target.depth > depth?"none":""})
   .attr("d", diagonal);

}

