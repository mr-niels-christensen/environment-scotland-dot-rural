function _updateSearchFromJson(response) {
  $ ( "#searchResults .datarow" ).remove();
  $.each(response.results, function(index, result){
    $( "#searchResults tr:last" ).after( "<tr class='searchResultRow'></tr>" );
    $( "#searchResults tr:last" ).append( "<td>" + result.snippet + "</td>" );
    $( "#searchResults tr:last" ).append( "<td class='sepakeUri hiddenColumn'>" + result.uri + "</td>" );
  });
  $( "#searchResults .searchResultRow" ).on( 'click', function() {
    var uri = $( this ).find( '.sepakeUri' ).text();
    console.log(uri)
  });
}

//For alternative methods, see http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
var match = RegExp('[?&]' + 'query' + '=([^&]*)').exec(window.location.search);
var query = match && decodeURIComponent(match[1].replace(/\+/g, ' '));
query = query || '';
search(query, _updateSearchFromJson);

