
var desc = document.getElementById("description");
var addchangedesc = function(e){
    desc.addEventListener('click', change);
}
var revdesc = function(e) {
    console.log('?');
    var newdesc = document.getElementById("descentry").value;
    desc.innerHTML = newdesc;
    setTimeout(addchangedesc,1);
    
};

var change = function(e) {
    
    desc.innerHTML = '<textarea rows="4" cols="50" id="descentry">' + desc.innerHTML + '</textarea><br><button id = "subdesc" > Submit </button><br>';
    var sub = document.getElementById("subdesc");
    desc.removeEventListener('click', change);
    sub.addEventListener('click', revdesc);
    
};

desc.addEventListener('click', change);


		$("button#save").click(function() {
			var data = {};
			data.templatehtml = document.getElementsByTagName("html")[0];
		$.ajax({
			type: "POST",
			url: "/save",
			contentType: "application/json",
			data: JSON.stringify(data)/*,
			success: function(data){
				var res = data['name']
				$('.container').html(res)},
			error: function(data){
				$('#result').html('I failed')
			}
			*/
		})/*
            var firstName = document.getElementById("inputFirstName").value;
            var lastName = document.getElementById("inputLastName").value;
            var name = firstName + lastName;
            window.location.href= 'home/' + name;
            */
		})

