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

function getStudentId() {
  // Select the input element with the name "student_id"
  const studentIdInput = document.querySelector('input[name="student_id"]');

  if (studentIdInput) {
      // Access the value of the "student_id" input
      const studentId = studentIdInput.value;
      return studentId;
  } else {
      // Handle the case where the input is not found
      console.error('Student ID input not found.');
      return null;
  }
}


$(document).ready(function(){
  $(".inline_textarea_etat_situation").focusout(function(){
      var student_id = getStudentId();  // Use the getStudentId() function
      // Check if student_id is valid
      if (student_id !== null) {
          console.log("creation date", $(this).attr("data-creationdate"));
          var myContent = {
              student_id: student_id,
              creationDateStr: $(this).attr("data-creationdate"),
              post_id: $(this).attr("id"),
              etatdelasituation: tinymce.activeEditor.getContent(),
              csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          };

          console.log("data sent", myContent);

          $.ajax({
              method: "POST",
              url: "http://127.0.0.1:8000/etudiant/detail/" + student_id,
              dataType: "json",
              data: myContent,
              success: function(data){
                  console.log("data received", data);
              },
          });
      } else {
          console.error('Invalid student ID.');
      }
  });
});
