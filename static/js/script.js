$(document).ready(function() {
  $("#btnFetch").click(function() {
    console.log('pinchado');
    $('#spinner').show();
  });


  if ($("#transcripcion").length > 10){
    $('#spinner').hide();
  }

});