function _updateSearchFromJson(response) {
  $ ( "#searchResults .dynamicrow" ).remove();
  $.each(response.results, function(index, result){
    $( "#searchResults tr:last" ).after( "<tr class='searchResultRow dynamicrow'></tr>" );
    $( "#searchResults tr:last" ).append( "<th>" + result.label + "</th>" );
    $( "#searchResults tr:last" ).append( "<td class='sepakeUri hiddenColumn'>" + result.uri + "</td>" );
    $( "#searchResults tr:last" ).after( "<tr class='searchResultRow dynamicrow'></tr>" );
    $( "#searchResults tr:last" ).append( "<td>" + (result.description || "") + "</td>" );
    $( "#searchResults tr:last" ).append( "<td class='sepakeUri hiddenColumn'>" + result.uri + "</td>" );
  });
  $( "#searchResults .searchResultRow" ).on( 'click', function() {
    var iri = encodeURI($( this ).find( '.sepakeUri' ).text());
    var link_url = jQuery.param.fragment( '/focus.html', {'iri' : iri} );
    document.location.href = link_url;
  });
  if (response.next_cursor_websafe) {
    $( "#searchResults tr:last" ).after( "<tr class='dynamicrow'><td><a class='moreLink'>More...</a></td></tr>" );
    var more_url = jQuery.param.fragment( '/search.html', {'query' : response.query, 'cursor_websafe' : response.next_cursor_websafe} );
    $( "#searchResults .moreLink" ).attr('href', more_url);
  }
}

function _updateSearchFromHashChange(event) {
  var query = event.getState( 'query' ) || '';
  var cursor_websafe =  event.getState( 'cursor_websafe' ) || null;
  search(query, cursor_websafe, _updateSearchFromJson);
}

$(window).bind( 'hashchange', _updateSearchFromHashChange);
$(window).trigger( 'hashchange' );
