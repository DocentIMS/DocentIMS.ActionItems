var $jq = jQuery.noConflict();
var $ = jQuery.noConflict();

$jq(document).ready(function () {

  // Scope analysis, hide show fields. 
  // Shows and hides fields depending on checkbox

  if ($jq('#form-widgets-internal_qc_required_-0').is(':checked')) {
    // $('#formfield-form-widgets-estimated_qc_time, #formfield-form-widgets-notes_to_qc').show();
  } else {
    $jq('#formfield-form-widgets-estimated_qc_time, #formfield-form-widgets-notes_to_qc, #formfield-form-widgets-finishing_date_for_qc, #formfield-form-widgets-date_wc_finished, #formfield-form-widgets-date_item_finished').hide();
  }

  $jq('#form-widgets-internal_qc_required_-0').change(function () {
    $jq('#formfield-form-widgets-estimated_qc_time, #formfield-form-widgets-notes_to_qc, #formfield-form-widgets-finishing_date_for_qc, #formfield-form-widgets-date_wc_finished, #formfield-form-widgets-date_item_finished').toggle();
  });


  if ($jq('#form-widgets-is_the_analyis_complete-0').is(':checked')) {
    //$('#formfield-form-widgets-analysis_notes').show();
  } else {
    $jq('#formfield-form-widgets-analysis_notes').hide();
  }

  $jq('#form-widgets-is_the_analyis_complete-0').change(function () {
    $jq('#formfield-form-widgets-analysis_notes').toggle();
  });

  // end

  if ($jq('#form-widgets-is_this_action_out_of_the_scope_of_work_-0').not(':checked')) {
    $jq('#formfield-form-widgets-explanation_for_out_of_scope_ai').hide();

  } else {
    $jq('#formfield-form-widgets-related_sow_section, #sow_section_text').hide();
  }
  $jq('#formfield-form-widgets-is_this_action_out_of_the_scope_of_work_ input').change(function () {
    if ($jq('#form-widgets-is_this_action_out_of_the_scope_of_work_-0').is(':checked')) {
      $jq('#formfield-form-widgets-explanation_for_out_of_scope_ai').show();
      $jq('#formfield-form-widgets-related_sow_section, #section_text').hide();
    }
    else {
      $jq('#formfield-form-widgets-explanation_for_out_of_scope_ai').hide();
      $jq('#formfield-form-widgets-related_sow_section, #sow_section_text').show();
    }
  });
  if ($jq('#form-widgets-is_this_item_closed-0 input').not(':checked')) {
    $jq('#formfield-form-widgets-actions_to_close_out').hide();
  }
  $jq('#form-widgets-is_this_item_closed-0').change(function () {
    if ($jq('#form-widgets-is_this_item_closed-0').is(':checked')) {
      $jq('#formfield-form-widgets-actions_to_close_out').show();
    }
    else {
      $jq('#formfield-form-widgets-actions_to_close_out').hide();
    }
  });

  $jq('#form-widgets-related_sow_section').on("change", function () {
    if ($jq(this).val() != '--NOVALUE--') {
      $jqsearchval = $jq('body').attr("data-portal-url") + '/@search?fullobjects=1&UID=' + $jq(this).val();

      $jq.ajax({
        url: $jqsearchval,
        contentType: "application/json",
        dataType: 'json',
        headers: { 'Accept': 'application/json' },
        success: function (result) {
          //console.log(result.items[0]);
          $jq('#sow_text_add').remove();
          $jq("#formfield-form-widgets-related_sow_section").append('<div id="sow_text_add"><hr/>' + result.items[0].bodytext.data + '</div>');
        }
      })
    }
  });
});
