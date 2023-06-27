$(document).ready(function() {
  if( $('#form-widgets-is_this_action_out_of_the_scope_of_work_-0').is(':checked') ) {
      $('#formfield-form-widgets-explanation_for_out_of_scope_ai').hide();
  }
  $('#formfield-form-widgets-is_this_action_out_of_the_scope_of_work_ input').change(function () {
      if( $('#form-widgets-is_this_action_out_of_the_scope_of_work_-0').is(':checked') ) {
          $('#formfield-form-widgets-explanation_for_out_of_scope_ai').hide();
      }
      else {
          $('#formfield-form-widgets-explanation_for_out_of_scope_ai').show();
      }
  });
});
