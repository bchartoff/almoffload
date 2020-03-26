d3.json("static/data/tasks.json?_=" + new Date().getTime()).then(function(tasks){
	console.log(tasks.nat.daily)
	d3.select("body")
		.on("click", function(){
			tasks.nat.daily.push("a")
			// console.log(tasks)

	      $.ajax({
	          type: 'POST',
	          url: '/update-tasks',
	          data: JSON.stringify(tasks),
				dataType: 'json',
contentType: 'application/json; charset=utf-8',
	          success: function(data) {
	              // $("#federal_public_employment-status")
	              //   .css("opacity",1)
	              //   .text("Federal public employment data uploaded")
	              console.log(data)
	          },
	          fail: function(e){
	            alert("Something went wrong uploading the file, try reloading the page and trying again")
	          }
	      });


		})
})
