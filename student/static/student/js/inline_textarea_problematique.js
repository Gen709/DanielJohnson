const inline_textarea_problematique = {
selector: '.inline_textarea_problematique',
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

tinymce.init(inline_textarea_problematique);

$(document).ready(function(){
    // get info on select

    $(".inline_textarea_problematique").click(function() {
        problematique_id = this.id ;
        console.log(problematique_id);

        $('#' + problematique_id ).focusout(function(){
            var myContent = {problematique_id: problematique_id,
                             problematique_desc: tinymce.get(problematique_id).getContent()
                             //csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                        };
            console.log(myContent);
            $.ajax({
                method:"POST",
                url: "http://127.0.0.1:8000/etudiant/problematique/ajax/update",
                dataType: "json",
                data:myContent,
                    success: function(data){
                        console.log(data);
                    },
            });
        });
    });
});