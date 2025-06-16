jQuery(document).ready(function() {
  // Check stored state
  if (localStorage.getItem("toolbarHidden") === "true") {
      jQuery("#toolbar").hide();
      jQuery("#show-toobar").removeClass('hidden');
      jQuery("#show-toobar").show();
      
  } else {
      jQuery("#show-toobar").hide();
  }

  jQuery("#hide-toolbar, #show-toobar").click(function() {
      jQuery("#toolbar, #show-toobar").slideToggle();
      jQuery("#show-toobar").removeClass('hidden');
      
      // Update state in localStorage
      const isHidden = (localStorage.getItem("toolbarHidden") === "true");
      localStorage.setItem("toolbarHidden", !isHidden);
  });
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