$(document).ready(function() {
  if( $('#form-widgets-is_this_action_out_of_the_scope_of_work_-0').not(':checked') ) {
      $('#formfield-form-widgets-explanation_for_out_of_scope_ai').hide();

  } else {
    $('#formfield-form-widgets-related_sow_section, #formfield-form-widgets-sow_section_text').hide();
  }
  $('#formfield-form-widgets-is_this_action_out_of_the_scope_of_work_ input').change(function () {
      if( $('#form-widgets-is_this_action_out_of_the_scope_of_work_-0').is(':checked') ) {
          $('#formfield-form-widgets-explanation_for_out_of_scope_ai').show();
          $('#formfield-form-widgets-related_sow_section, #formfield-form-widgets-sow_section_text').hide();
      }
      else {
        $('#formfield-form-widgets-explanation_for_out_of_scope_ai').hide();
        $('#formfield-form-widgets-related_sow_section, #formfield-form-widgets-sow_section_text').show();
      }
  });
  if( $('#form-widgets-is_this_item_closed-0 input').not(':checked') ) {
      $('#formfield-form-widgets-actions_to_close_out').hide();
  }
  $('#form-widgets-is_this_item_closed-0').change(function () {
    if( $('#form-widgets-is_this_item_closed-0').is(':checked') ) {
          $('#formfield-form-widgets-actions_to_close_out').show();
      }
      else {
          $('#formfield-form-widgets-actions_to_close_out').hide();
      }
  });
});
