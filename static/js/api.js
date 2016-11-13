$(document).ready(function(){
	$(".submit").click(function(){
		var query = $("#query").val();
		$("#response").html('');
		console.log(query);
		if(query != ""){
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
			    		$("#response").html(data["line"] + "<br>" + (data["unsure"] ? "Might I suggest some " + data["cheese"] + " and a bottle of " + data["wine"] + " to wash down your sorrows?" : "Try some " + data["cheese"] + " to go with your " + data["wine"] + " and relax!"));
			    	}else if (data["line"] != ""){
			    		$("#response").html(data["line"]);
			    	}else if (data["cheese"] != ""){
						$("#response").html(data["unsure"] ? "How about some " + data["cheese"] + " cheese and a bottle of " + data["wine"] + "?" : "Try some " + data["cheese"] + " to go with your " + data["wine"] + " and relax!");
			    	}else{
			    		$("#response").html('Uh-huh, yes, I see. Tell me more...');
			    	}
			    },
			    error: function(data){
			        console.log(data);
			    }
			});
		}
		function drawMood(mood){
			$("#logo").remove();
			$("#logoDiv").append('<img id="logo" src="../static/images/' + mood + '.png">');
		}
	});
});
