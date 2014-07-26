
$(document).ready(function(){
	$('#email').change(function(){
		var email = $('#email').val();

		$.ajax({
			url:'/email_check?email='+email,
			type:'POST',
			data:{"email":email}, /*이렇게 하면 데이터를 보내는 중!//보낼 소포*/
			success:function(response){/*요청한 것에 대한 응답이 response 에 들어온다*/
				var json_name = $.parseJSON(data);
				console.log(json['message']);
				console.log("Okay");
			},
			error:function(){
				console.log('error');
			},
			complete:function(){
				console.log('complete');
			}
			

		});

	});

});