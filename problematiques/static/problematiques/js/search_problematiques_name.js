
$(document).ready(function(){
	$("#studentsearchbox").keyup(function(){
		$.ajax({
		url: "http://127.0.0.1:8000/problematiques/ajax/",
		dataType: "json",
		data:'term='+$(this).val(),
		
			success: function(data){
				//console.log(data)
				
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
				
				$("#suggesstion-box").show();
				$("#suggesstion-box").html(html_str);
					
			}
		});	
	});
});


function selectStudent(student_desc, student_id) {
	//console.log(typeof student_id);
	$("#problematique_suggestion_box").val(student_id);
	//$('input[class="student_id"]').val(student_id);
	$("#problematique_suggestion_box").val(student_desc);
	$("#suggesstion-box").hide();
};