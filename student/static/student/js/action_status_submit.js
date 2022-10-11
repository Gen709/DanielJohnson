$(document).ready(function(){
    $(".action-status-select-js").change(function(){
        var myContent = {action_id: this.id,
                         status_id: this.value
                             //csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                        };
         console.log(myContent)
         $.ajax({
            method:"POST",
            url: "http://127.0.0.1:8000/etudiant/problematique/action/status/ajax/update",
            dataType: "json",
            data:myContent,
                success: function(data){
                    console.log(data);
                },
        });

    });

});