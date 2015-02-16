//For alternative methods, see http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

$( document ).ready( function() {
  $( "#askButton" ).click(function() {
    //var url = encodeURI('https://twitter.com/intent/tweet?screen_name=niels_may_acs&text=' + $( '#questionText' ).val());
    var url = encodeURI(
        'http://earthscience.stackexchange.com/questions/ask?tags=environment scotland&title=' 
        + $( '#questionText' ).text()
    );
    $( this ).attr( "href", url );
  });
  var ask = getParameterByName('ask');
  if (ask == 'on') {
    $( '#askPanel' ).show();  
  };
});
