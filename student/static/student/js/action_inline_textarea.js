const inline_textarea_action_detail = {
selector: '.inline_textarea_action_detail',
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

tinymce.init(inline_textarea_action_detail);

$(document).ready(function(){

    $(".inline_textarea_action_detail").click(function() {
        var action_id = this.id;

        $('#' + action_id ).focusout(function(){

            var myContent = {action_id: action_id,
                             action_desc: tinymce.get(action_id).getContent()
                             };

            console.log(myContent);
            $.ajax({
                method:"POST",
                url: "http://127.0.0.1:8000/etudiant/problematique/action/detail/ajax/update",
                dataType: "json",
                data:myContent,
                    success: function(data){
                        console.log(data);
                    },
            });
        });
    });
});