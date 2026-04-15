// Allow opening and closing the burger menu when the button is clicked.
$(document).ready(function(){
    $('.header__burger').click(function(event){
        $('.header__burger, .header__menu').toggleClass('active');
        $('body').toggleClass('lock');
    });
    // Close the burger menu when an anchor link is clicked.
    $('.nav-link').click(function(event){
        $('.header__burger, .header__menu').removeClass('active');
        $('body').removeClass('lock');
    });

});
