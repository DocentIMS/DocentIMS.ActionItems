

$(document).ready(function() {


// Scope analysis, hide show fields. 
// Shows and hides fields depending on checkbox

if( $('#form-widgets-internal_qc_required_-0').is(':checked') ) {
  // $('#formfield-form-widgets-estimated_qc_time, #formfield-form-widgets-notes_to_qc').hide();
} else {
  $('#formfield-form-widgets-estimated_qc_time, #formfield-form-widgets-notes_to_qc').hide();
}

$('#form-widgets-internal_qc_required_-0').change(function () {
  $('#formfield-form-widgets-estimated_qc_time, #formfield-form-widgets-notes_to_qc').toggle();
});


if( $('#form-widgets-is_the_analyis_complete-0').is(':checked') ) {
    //$('#formfield-form-widgets-analysis_notes').show();
} else {
  $('#formfield-form-widgets-analysis_notes').hide();
}

$('#form-widgets-is_the_analyis_complete-0').change(function () {
  $('#formfield-form-widgets-analysis_notes').toggle();
});

// end

  if( $('#form-widgets-is_this_action_out_of_the_scope_of_work_-0').not(':checked') ) {
      $('#formfield-form-widgets-explanation_for_out_of_scope_ai').hide();

  } else {
    $('#formfield-form-widgets-related_sow_section, #sow_section_text').hide();
  }
  $('#formfield-form-widgets-is_this_action_out_of_the_scope_of_work_ input').change(function () {
      if( $('#form-widgets-is_this_action_out_of_the_scope_of_work_-0').is(':checked') ) {
          $('#formfield-form-widgets-explanation_for_out_of_scope_ai').show();
          $('#formfield-form-widgets-related_sow_section, #section_text').hide();
      }
      else {
        $('#formfield-form-widgets-explanation_for_out_of_scope_ai').hide();
        $('#formfield-form-widgets-related_sow_section, #sow_section_text').show();
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

  $('#form-widgets-related_sow_section').on( "change", function() {
    if ($( this ).val() != '--NOVALUE--' )     {
      $searchval = $('body').attr("data-portal-url") + '/@search?fullobjects=1&UID='+ $( this ).val() ;

      $.ajax({
        url: $searchval,
        contentType: "application/json",
        dataType: 'json',
        headers: {'Accept': 'application/json'},
        success: function(result){
          //console.log(result.items[0]);
          $('#sow_text_add').remove();
          $( "#formfield-form-widgets-related_sow_section").append('<div id="sow_text_add"><hr/>' + result.items[0].bodytext.data + '</div>');
        }
      })
  }
});
});
