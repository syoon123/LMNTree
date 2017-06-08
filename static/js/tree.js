var data = document.getElementById("data").innerHTML;

var table = d3.csvParse(data, function(d,i){
    return{
	id: d.Course,
	parentId: d.Prereq,
	selected:false};
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
function update(source) {
    var depth = 1
    var updatebuttons = function(){
	for(i = depth; i<= depth; i++){
	    svg.append("circle").attr('class','buttons').attr('r',30).attr('x', 180).attr('y', 15).attr('selected',false).style("fill","green").attr('transform', 'translate(' + (i * 180) + ",0)").on('click', function(){
		var tally = 0;
		source.descendants().forEach(
		    function(d){
			d.depth - depth == -1 && d.selected?tally++:tally+=0;
		    });
		if (depth > 1 && (tally < 7 || tally > 10)){
		    console.log(tally);
		    alert('please select between 7 and 10 classes');
		    return;
		};
		depth += 1;
		updatebuttons();
		updatenodes();
		updatetree();
		this.parentElement.removeChild(this);
	    }).append("text")
		.attr('x',0).attr('y',0)
		.attr("dy", ".35em")
		.attr('transform', 'translate(' + (i * 180) + ",0)")
		.attr("text-anchor", function(d) { 
		    return "start"; })
		.text(function(d) { return 'next'; })
		.style("fill-opacity", 1).style('font-color','white');
	};
    };
    updatebuttons();
    var nodes = tree.nodes(root).reverse(),
	links = tree.links(nodes);
    var updatenodes = function(){
	newroot = source;
	newroot.descendants().forEach(function(d){//console.log(d.depth)});};
	    if (d.depth >= depth ) {
		d._children = d.children;
		d.children = null;
	    }else if (!d.selected){
		d._children = d.children;
		d.children = null;
	    }else{
		console.log(d);
	//	d.parent?d.parent.children.forEach(function(f){!f.selected?d._children.push(f):true}):true;
		d.children = d.children?d.children:d._children;
	    };
	});
	nodes = tree.nodes(newroot);
	console.log(nodes);
	links = tree.links(nodes);
	source = newroot;
    };
    updatenodes();
    
    //var updatenodes = function(){
	
							  
    // Normalize for fixed-depth.
    var updatetree = function(){
	nodes.forEach(function(d) { d.y = d.depth * 180; });
	links.forEach(function(d){console.log(d)});// Declare the nodes
	
	var node = svg.selectAll("g.node")
	    .data(nodes, function(d) { return d.id || (d.id = ++i); });

	var updatecolor = function(){
	    d3.selectAll('rect').transition().duration(300).style("fill",function(d){return d.selected?"green":"#fff";});
	};
	// Enter the nodes.

	var nodeEnter = node.enter().append("g")
	    .attr("class", "node")
	    .on('click', function(d){d.selected = d.selected?false:true; updatecolor() } ) 
	    .attr("transform", function(d) { 
		return "translate(" + d.y + "," + d.x + ")"; });

	nodeEnter.append("rect")
	    .attr("width", function(d){ return d.id.split('').length * 6;})
	    .attr("height", 20).attr("y",-10)
	    .style("fill",function(d){return d.selected?"green":"#fff";})
	    .style("stroke-width","1")
	    .style("stroke","rgb(0,0,0)");

	nodeEnter.append("text")
	    .attr("x", function(d) { 
		return 2 })
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
	    .attr("d", diagonal);
    };
    updatetree();

}

