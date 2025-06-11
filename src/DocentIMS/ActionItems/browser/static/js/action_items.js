document.addEventListener("DOMContentLoaded", function () {
  const portalUrl = document.body.getAttribute("data-portal-url");

  // Helper functions
  function isChecked(selector) {
    const el = document.querySelector(selector);
    return el && el.checked;
  }

  function toggleDisplay(selectors, show) {
    selectors.forEach(selector => {
      const el = document.querySelector(selector);
      if (el) el.style.display = show ? "" : "none";
    });
  }

  // Initial setup for internal QC checkbox
  const qcCheckbox = document.querySelector('#form-widgets-internal_qc_required_-0');
  const qcFields = [
    '#formfield-form-widgets-estimated_qc_time',
    '#formfield-form-widgets-notes_to_qc',
    '#formfield-form-widgets-finishing_date_for_qc',
    '#formfield-form-widgets-date_wc_finished',
    '#formfield-form-widgets-date_item_finished'
  ];

  if (!isChecked('#form-widgets-internal_qc_required_-0')) {
    toggleDisplay(qcFields, false);
  }

  if (qcCheckbox) {
    qcCheckbox.addEventListener("change", () => {
      qcFields.forEach(selector => {
        const el = document.querySelector(selector);
        if (el) el.style.display = el.style.display === "none" ? "" : "none";
      });
    });
  }

  // Analysis complete field
  const analysisField = '#formfield-form-widgets-analysis_notes';
  if (!isChecked('#form-widgets-is_the_analyis_complete-0')) {
    toggleDisplay([analysisField], false);
  }

  const analysisCheckbox = document.querySelector('#form-widgets-is_the_analyis_complete-0');
  if (analysisCheckbox) {
    analysisCheckbox.addEventListener("change", () => {
      const el = document.querySelector(analysisField);
      if (el) el.style.display = el.style.display === "none" ? "" : "none";
    });
  }

  // Out of scope logic
  const outOfScopeInput = document.querySelector('#form-widgets-is_this_action_out_of_the_scope_of_work_-0');
  if (outOfScopeInput) {
    if (!outOfScopeInput.checked) {
      toggleDisplay(['#formfield-form-widgets-explanation_for_out_of_scope_ai'], false);
    } else {
      toggleDisplay(['#formfield-form-widgets-related_sow_section', '#sow_section_text'], false);
    }

    const scopeWrapper = document.querySelector('#formfield-form-widgets-is_this_action_out_of_the_scope_of_work_');
    if (scopeWrapper) {
      scopeWrapper.addEventListener("change", () => {
        const checked = outOfScopeInput.checked;
        toggleDisplay(['#formfield-form-widgets-explanation_for_out_of_scope_ai'], checked);
        toggleDisplay(['#formfield-form-widgets-related_sow_section', '#sow_section_text'], !checked);
      });
    }
  }

  // Item closed logic
  const itemClosedCheckbox = document.querySelector('#form-widgets-is_this_item_closed-0');
  if (itemClosedCheckbox && !itemClosedCheckbox.checked) {
    toggleDisplay(['#formfield-form-widgets-actions_to_close_out'], false);
  }

  if (itemClosedCheckbox) {
    itemClosedCheckbox.addEventListener("change", () => {
      toggleDisplay(['#formfield-form-widgets-actions_to_close_out'], itemClosedCheckbox.checked);
    });
  }

  // AJAX for related SOW section
  const sowDropdown = document.querySelector('#form-widgets-related_sow_section');
  if (sowDropdown) {
    sowDropdown.addEventListener("change", function () {
      const uid = this.value;
      if (uid && uid !== '--NOVALUE--') {
        fetch(`${portalUrl}/@search?fullobjects=1&UID=${uid}`, {
          headers: { 'Accept': 'application/json' }
        })
        .then(response => response.json())
        .then(result => {
          const prev = document.getElementById('sow_text_add');
          if (prev) prev.remove();

          const container = document.getElementById("formfield-form-widgets-related_sow_section");
          if (container && result.items[0]) {
            const div = document.createElement("div");
            div.id = "sow_text_add";
            div.innerHTML = `<hr/>${result.items[0].bodytext.data}`;
            container.appendChild(div);
          }
        });
      }
    });
  }

  // HTML tooltips
  document.querySelectorAll('.htmltooltip').forEach(el => {
    const content = el.getAttribute('data-tooltip-content');
    el.setAttribute('title', content);
    // Tooltips depend on UI library; for vanilla JS you'd need a tooltip system or rely on title
  });

  // Toolbar logic
  const toolbar = document.getElementById("toolbar");
  const showToolbarBtn = document.getElementById("show-toobar");

  if (localStorage.getItem("toolbarHidden") === "true") {
    if (toolbar) toolbar.style.display = "none";
    if (showToolbarBtn) {
      showToolbarBtn.classList.remove("hidden");
      showToolbarBtn.style.display = "";
    }
  } else if (showToolbarBtn) {
    showToolbarBtn.style.display = "none";
  }

  const hideToolbarBtn = document.getElementById("hide-toolbar");
  [hideToolbarBtn, showToolbarBtn].forEach(btn => {
    if (btn) {
      btn.addEventListener("click", () => {
        if (toolbar) toolbar.classList.toggle("hidden");
        if (showToolbarBtn) showToolbarBtn.classList.remove("hidden");
        const hidden = localStorage.getItem("toolbarHidden") === "true";
        localStorage.setItem("toolbarHidden", !hidden);
      });
    }
  });

  // Meeting select highlight
  const meetingSelect = document.getElementById("meeting_select");
  if (meetingSelect) {
    meetingSelect.addEventListener("change", () => {
      document.querySelectorAll('#meeting_select a').forEach(a => a.classList.toggle("greyed"));
    });
  }

  // Create meeting select
  const createMeeting = document.getElementById("create_meeting");
  if (createMeeting) {
    createMeeting.addEventListener("change", function () {
      if (this.value === "create_meeting") {
        window.location.href = portalUrl + "/meetings/++add++meeting";
      } else if (this.value === "your_meetings") {
        document.querySelectorAll('#meeting_select a').forEach(a => a.classList.toggle("greyed"));
        window.location.href = portalUrl + "/meetings/meeting-collection";
      }
    });
  }

  // Show manager toolbar if applicable
  if (localStorage.getItem("isManager") === "true") {
    document.querySelectorAll('.toolbar_user, .toolbar_manager').forEach(el => el.classList.toggle("hidden"));
    if (toolbar) toolbar.classList.toggle("manager_mode");
  }

  // Toggle toolbar mode
  document.querySelectorAll('#toolbar_mode a').forEach(a => {
    a.addEventListener("click", () => {
      document.querySelectorAll('.toolbar_user, .toolbar_manager').forEach(el => el.classList.toggle("hidden"));
      if (toolbar) toolbar.classList.toggle("manager_mode");
      const manager = localStorage.getItem("isManager") === "true";
      localStorage.setItem("isManager", !manager);
    });
  });

  // Show comment form controls
  const commentText = document.getElementById("form-widgets-comment-text");
  if (commentText) {
    commentText.addEventListener("click", () => {
      document.querySelectorAll(".pat-discussion .formControls").forEach(fc => {
        fc.style.display = "";
      });
    });
  }
});


jQuery(document).ready(function() {
  if ($("#portal-column-two").length) {
        $("#toggle-filters").removeClass("hidden"); 
    }
  jQuery("#portal-column-two").hide();
  jQuery("button#toggle-filters").click(function() {
    jQuery("#portal-column-two").slideToggle();
    jQuery("#portal-column-two").toggleClass("overlay");              
  });
}); 