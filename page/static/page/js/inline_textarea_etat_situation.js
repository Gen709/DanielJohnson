const inline_textarea_etat_situation = {
  selector: '.inline_textarea_etat_situation',
  menubar: false,
  inline: true,
  plugins: [
    'link', 'lists',
    'autolink'
  ],
  toolbar: [
    'undo redo | bold italic underline | fontfamily fontsize',
    'forecolor backcolor | alignleft aligncenter alignright alignfull | numlist bullist outdent indent'
  ],
  valid_elements: 'p[style], strong, em, span[style], a[href], ul, ol, li',
  valid_styles: {
    '*': 'font-size,font-family,color,text-decoration,text-align'
  },
  powerpaste_word_import: 'clean',
  powerpaste_html_import: 'clean',
};

tinymce.init(inline_textarea_etat_situation);

$(document).ready(function(){
	$("#inline_textarea_etat_situation").focusout(function(){
		var myContent = {student_id: $('#student_id').val(), 
						 etatdelasituation: tinymce.get("inline_textarea_etat_situation").getContent(),
						 csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
						 };

        console.log(myContent);

		$.ajax({
            method:"POST",
            url: "http://127.0.0.1:8000/etudiant/ajax/etatdelasituation/",
            dataType: "json",
            //data:'etatdelasituation='+myContent,
            data:myContent,
            success: function(data){
                console.log(data);
            },
		});
	});
});