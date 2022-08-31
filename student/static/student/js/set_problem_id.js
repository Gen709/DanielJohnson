$(document).on("click", ".open-action", function (){
	var probleme_id = $(this).data('id');
	$(".modal-body #problematique_id").val(probleme_id);
	
	$("#description").keyup(function(){
		$.ajax({
		url: "http://127.0.0.1:8000/etudiant/ajax/action/suggestions",
		dataType: "json",
		data:'term='+$(this).val(),
		
			success: function(data){
				console.log(data)
				
				var html_str ;
				html_str = '<ul class="list-group" id="student-list">';
				
				for (let key in data) {
				  let value = data[key];
				  
				  for (student_id in value){
					
				  	let info=value[student_id];
						
				  		var student_desc = info.description;
						
				  		html_str +=  '<li class="list-group-item list-group-flush" onClick="selectStudent(\''+ student_desc.replaceAll('\'', '') + '\', ' + student_id + ', 1)">'  + student_desc.replaceAll('\'', '') +'</li>';
				  } 
				}	
					
				html_str += '</ul>';	
				
				$("#ajax-action-suggestions").show();
				$("#ajax-action-suggestions").html(html_str);
					
			}
		});	
	});
});

function selectStudent(student_desc, student_id) {
	//console.log(typeof student_id);
	//$("#ajax-action-suggestions").val(student_id);
	//$('input[class="student_id"]').val(student_id);
	$("#description").val(student_desc);
	$("#ajax-action-suggestions").hide();
};