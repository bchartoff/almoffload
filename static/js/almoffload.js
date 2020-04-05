function initBoorger(){
	var svg = d3.select(".settingsContainer")
		.append("svg")
		// .attr("class","open")
		.attr("width", 44)
		.attr("height", 44)

	var data = [0,1,2]
	svg.selectAll(".boorg")
		.data(data)
		.enter()
		.append("line")
		.attr("class","boorg")
		.attr("x1",4)
		.attr("x2",36)
		.attr("y1", function(d){ return 8 + d*14})
		.attr("y2", function(d){ return 8 + d*14})
		.attr("stroke", "#353535")
		.attr("stroke-width", "4px")
		.attr("fill", "none")
		.attr("stroke-linecap","round")

}

function toggleMenu(){
	var svg = d3.select(".settingsContainer svg")
	if(svg.classed("open")){
		d3.selectAll(".boorg")
			.transition()
		.attr("y1", function(d){ return 8 + d*14})
		.attr("y2", function(d){ return 8 + d*14})
		
		d3.select("#controlContainer")
			.transition()
			.style("right", "-320px")
		
		svg.classed("open",false)
	}else{
		d3.selectAll(".boorg")
			.transition()
			.attr("y1", function(d){ return (d == 1) ? 8 : 8 + d*14 })
			.attr("y2", function(d){
				if(d == 1 || d == 0) return 8 + 2*14
				else return 8
			})
		d3.select("#controlContainer")
			.transition()
			.style("right", "0px")


		
		svg.classed("open",true)
	}

}


function getName(){

}



function init(tasks, preferences){
	console.log(tasks, preferences)
	initControls(preferences)
	initBoorger()
}
function initControls(preferences){
	if(name == "ben"){
		d3.select(".name.button.nat").classed("disabled",true)
		d3.select(".hidden.button").classed("disabled", !preferences.ben.showHidden)
		d3.select(".complete.button").classed("disabled", !preferences.ben.showCompleted)
	}
	else if(name == "nat"){
		d3.select(".name.button.ben").classed("disabled",true)
		d3.select(".hidden.button").classed("disabled", !preferences.nat.showHidden)
		d3.select(".complete.button").classed("disabled", !preferences.nat.showCompleted)
	}else{
		d3.select(".hidden.button").classed("disabled", true)
		d3.select(".complete.button").classed("disabled", true)
	}
	d3.selectAll(".button")
		.style("opacity",1)
		.on("click", function(){
			if(d3.select(this).classed("disabled")){
				d3.select(this).classed("disabled", false)
			}else{
				d3.select(this).classed("disabled", true)
			}
		})
	d3.select(".settingsContainer").on("click", toggleMenu)


}


function updateTaskJson(tasks){
	$.ajax({
		type: 'POST',
		url: '/update-tasks',
		data: JSON.stringify(tasks),
		dataType: 'json',
		contentType: 'application/json; charset=utf-8',
		success: function(data) {
			console.log("Json updated", data);
		},
		fail: function(e){
			alert("Something went wrong", e);
		}
	});
}



d3.json("static/data/tasks.json?_=" + new Date().getTime()).then(function(tasks){
	d3.json("static/data/preferences.json?_=" + new Date().getTime()).then(function(preferences){
		init(tasks, preferences)
	})
})

