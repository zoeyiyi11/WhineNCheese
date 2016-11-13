$(document).ready(function(){
	$(".submit").click(function(){
		var query = $("#query").val();
		$("#response").html('');
		console.log(query);
		$.ajax({
		    url: '/process',
		    dataType: 'json',
		    type: 'POST',
		    contentType: 'application/json; charset=utf-8',
		    data: JSON.stringify({
		    	'query': query
		    }),
		    success: function(data){
		    	
		    	drawMood(data["mood"]);
		    	if(data["line"] != "" && data["cheese"] != ""){
		    		$("#response").html(data["line"] + "<br>" + "Try some " + data["cheese"] + " to go with your " + data["wine"] + " and relax!");
		    	}else if (data["line"] != ""){
		    		$("#response").html(data["line"]);
		    	}else if (data["cheese"] != ""){
					$("#response").html("Try some " + data["cheese"] + " to perfectly pair with your " + data["wine"] + "!");
		    	}
		    },
		    error: function(data){
		        console.log(data);
		    }
		});

		function drawMood(mood){
			$("#logo").remove();
		    $("#logoDiv").append('<img id="logo" src="../static/images/' + mood + '.png">');
		}

	});
});