
$(document).ready(function(){


	$("[name=email]").change(function(){
		
		if (!$(this).val().match(/[\w\d._]+@[\w\d-]+\.(\w{2,3}|\w{2}\.\w{2})/)) {
			$('#email').show();		

		}
		if ($(this).val().match(/[\w\d._]+@[\w\d-]+\.(\w{2,3}|\w{2}\.\w{2})/)) {
			$('#email').hide();		

		}
	});

	$("[name=password]").change(function(){
		

		if (!$(this).val().match(/(?=.{8,20})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!#\$%&\?])/)) {
			$('#password').show();
		}
		if ($(this).val().match(/(?=.{8,20})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!#\$%&\?])/)) {
			$('#password').hide();
		}
	});

	$("[name=password_check]").change(function(){
		

		if ($(this).val()!=$("[name=password]").val()) {
			$('#password_check').show();
		}
		else {
			$('#password_check').hide();
		}
	});

});