$(document).ready(function(){
//    $(".form-select").change(function(){
    $('select[name="problematique-status"]').change(function(){
        var myContent = {problematique_id: this.id,
                         status_id: this.value
                             //csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                        };
         $.ajax({
            method:"POST",
            url: "http://127.0.0.1:8000/etudiant/problematique/status/ajax/update",
            dataType: "json",
            data:myContent,
                success: function(data){
                    console.log(data);
                },
        });

    });

});