$(document).ready(function(){
 
    //on scroll, show the back to top button
    $(window).scroll(function(){
        if($(window).scrollTop() >= 1){ //if user has scrolled the window
            $('.backToTop').fadeIn(500); // show the back to top button
        }else { // else if user is at the top already
            $('.backToTop').fadeOut(500); //hide the back to top button
        }
    });
 
    //scroll the page to the top if user clicks on the back to top button
    $('.backToTop').click(function(){
        $('html,body').animate({ scrollTop: 0 }, 'slow');
    });
 
    //checks if page was already scrolled down before load
    if($(window).scrollTop() >= 1){
        $('.backToTop').show(); // show the back to top button
    }
});