$(document).on("click", ".open-action", function (){
	var probleme_id = $(this).data('id');
	$(".modal-body #problematique_id").val(probleme_id);
});