
$(document).ready(function(){
	$("#studentsearchbox").keyup(function(){
		$.ajax({
		url: "http://127.0.0.1:8000/etudiant/ajax/",
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
						var student_detail_url = info.url
						//console.log(student_detail_url)
				  		html_str +=  '<li class="list-group-item list-group-flush" onClick="selectStudent(\''+ student_desc.replaceAll('\'', '') + '\', ' + student_id + ', 1)">'  + student_desc.replaceAll('\'', '') +'</li>';
				  } 
				}	
					
				html_str += '</ul>';	
				
				$("#suggestion-box").show();
				$("#suggestion-box").html(html_str);
					
			}
		});	
	});
});


function selectStudent(student_desc, student_id) {
	console.log(typeof student_id);
	$("#student_id").val(student_id);
	//$('input[class="student_id"]').val(student_id);
	$("#studentsearchbox").val(student_desc);
	$("#suggestion-box").hide();
	var url = "http://127.0.0.1:8000/etudiant/detail/" + student_id; 
	console.log(url)
	if (url) { // require a URL
              window.location = url; // redirect
          }
	
	
}