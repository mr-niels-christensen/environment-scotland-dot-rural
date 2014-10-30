$( document ).ready( function() {
  $( "#askButton" ).click(function() {
    //var url = encodeURI('https://twitter.com/intent/tweet?screen_name=niels_may_acs&text=' + $( '#questionText' ).val());
    var url = encodeURI(
        'http://earthscience.stackexchange.com/questions/ask?tags=environment scotland&title=' 
        + $( '#questionText' ).text()
    );
    $( this ).attr( "href", url );
  });
});
