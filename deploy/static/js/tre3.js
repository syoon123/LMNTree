var data = document.getElementById("data").innerHTML;
console.log(data);
var table = d3.csvParse(data, function(d,i){
    console.log(d);
    return{
	Course: d.Course,
	Prereqs: d.Prereq  };
});
console.log(table);

var root = d3.stratify()
    .id(function(d) { return d.Course; })
    .parentId(function(d) { return d.Prereqs; })
console.log(root)
var tree = d3.tree(root);
console.log(tree())
