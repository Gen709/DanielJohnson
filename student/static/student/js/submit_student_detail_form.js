

function update_student(parameter, value, student_id) {
  $.ajax({
		url: "http://127.0.0.1:8000/etudiant/ajax/update",
		dataType: "json",
		data:'param='+parameter+'&value='+value+'&student_id='+student_id,
			success: function(data){
				console.log(data)	
			}
		});
}


$(document).ready(function(){
	
	var student_id = $("input[name=student_id]").val();
	
	$('#plan_interventionRadioOptionsflexSwitchCheck').on('change', function() {
		let parameter = this.id;
		let value = 0
		if ($(this).is(':checked')){
			value=1
		}
		update_student(parameter, value, student_id);
    	//alert(parameter + " " + value + " " + student_id);
	});
	
	$('#comite_cliniqueflexSwitchCheck').on('change', function() {
		let parameter = this.id;
		let value = 0
		if ($(this).is(':checked')){
			value=1
		}
		update_student(parameter, value, student_id);
    	//alert(parameter + " " + value + " " + student_id);
	});
	
	
	$('select').on('change', function () {
	    //var optionSelected = $("option:selected", this);
		var parameter = this.name;
	    var value = this.value;
		update_student(parameter, value, student_id);
		//alert(parameter + " " + value +" "+student_id);
   
	});
	
	
})