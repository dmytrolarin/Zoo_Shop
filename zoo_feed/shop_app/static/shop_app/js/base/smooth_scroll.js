
$(document).ready(function(){
  // Add smooth scrolling for all links.
  $("a").on('click', function(event) {
   
    // Make sure `.hash` has a value before overriding the default behavior.
    if (this.hash !== "") {
      // Prevent the default anchor click behavior.
      event.preventDefault();
      // Store the hash.
      var hash = this.hash;

      // Use jQuery's animate() method to add smooth page scrolling.
      // The optional number (800) is the duration in milliseconds.
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 800, function(){

        // Add the hash (#) to the URL after scrolling completes.
        window.location.hash = hash;
      });
    } // End of the condition.
  });
});
