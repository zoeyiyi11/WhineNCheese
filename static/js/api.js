$(document).ready(function(){
	$(".submit").click(function(){
		var query = $("#query").val();
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
		        //$('#response').html(data["response"]);
		        console.log(data);
		    },
		    error: function(data){
		        //console.log( errorThrown );
		        console.log(data);
		    }
		});
	});
});