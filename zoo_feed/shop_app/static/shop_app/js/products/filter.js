// Open and close the filters panel.
$(document).ready(function(){
    $('.button-filters, .filter-close-icon, .screen-background').click(function(event){
        $('.filters').toggleClass('open'); 
        $('.screen-background').toggleClass('active');
        $('body').toggleClass('lock');
    });
    
});
