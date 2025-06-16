$(document).ready(function () {
  // Check stored state
  if (localStorage.getItem("toolbarHidden") === "true") {
    $("#toolbar").hide();
    $("#show-toobar").removeClass('hidden');
    $("#show-toobar").show();

  } else {
    $("#show-toobar").hide();
  }

  $("#hide-toolbar, #show-toobar").click(function () {
    $("#show-toobar").removeClass('hidden');
    $("#toolbar, #show-toobar").slideToggle();

    // Update state in localStorage
    const isHidden = (localStorage.getItem("toolbarHidden") === "true");
    localStorage.setItem("toolbarHidden", !isHidden);
  });

  if ($("#portal-column-two").length) {
    $("#toggle-filters").removeClass("hidden");
  }
  $("#portal-column-two").hide();
  $("button#toggle-filters").click(function () {
    $("#portal-column-two").slideToggle();
    $("#portal-column-two").toggleClass("overlay");
  });
}); 
