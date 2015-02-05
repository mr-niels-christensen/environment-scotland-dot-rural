var _NEXT_PAGE_HTML = '<button type="button" class="moreLink btn btn-default btn-lg"><span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span> Next page</button>';
_NEXT_PAGE_HTML = "<tr class='dynamicrow'><td><p align='right'>" + _NEXT_PAGE_HTML + "</p></td></tr>";

function _updateSearchFromJson(response) {
  window.scrollTo(0, 0);
  $ ( "#searchResults .dynamicrow" ).remove();
  var query = jQuery.bbq.getState( 'query' );
  if ( query ) {
    $( "#searchResults tr:last" ).after( "<tr class='dynamicrow'><td class='small'>Found " + response.number_found + " results for '" + query + "'</td></tr>" );
  }
  $.each(response.results, function(index, result){
    $( "#searchResults tr:last" ).after( "<tr class='searchResultRow dynamicrow'></tr>" );
    $( "#searchResults tr:last" ).append( "<td><h1>" + result.label + "</h1></td>" );
    $( "#searchResults tr:last td" ).append( "<p>" + (result.description || "Click for details") + "</p>" );
    if (result.rank == 1) {
        result.rank = "0-1";
    }
    $( "#searchResults tr:last td" ).append( "<p class='small'>" + result.rank + " views by last status</p>" );
    $( "#searchResults tr:last" ).append( "<td class='sepakeUri hiddenColumn'>" + result.uri + "</td>" );
    $( "#searchResults tr:last" ).append( "<td style='text-align: right'><img src='" + result.logo + "'></td>" );
  });
  $( "#searchResults .searchResultRow" ).on( 'click', function() {
    var iri = $( this ).find( '.sepakeUri' ).text();
    var link_url = jQuery.param.fragment( '/focus.html', {'iri' : iri} );
    document.location.href = link_url;
  });
  if (response.next_cursor_websafe) {
    $( "#searchResults tr:last" ).after( _NEXT_PAGE_HTML );
    var more_url = jQuery.param.fragment( '/search.html', {'query' : response.query, 'cursor_websafe' : response.next_cursor_websafe} );
    $( "#searchResults .moreLink" ).on( 'click', function() {
      document.location.href = more_url;
    });
  }
}

function _docReady_updateSearchFromJson(response) {
  $( document ).ready( function (){
    _updateSearchFromJson(response);
  });
}

function _updateSearchFromHashChange(event) {
  var query = event.getState( 'query' ) || 'environment';
  var cursor_websafe =  event.getState( 'cursor_websafe' ) || null;
  search(query, cursor_websafe, _docReady_updateSearchFromJson);
  if (event.getState( 'query' )) {
    var recent = JSON.parse($.localStorage.getItem('search_history_recent_list')) || [];
    var new_len = recent.unshift(event.getState( 'query' ));
    if (new_len > 10) {
      recent.pop();
    };
    console.log(recent);
    $.localStorage.setItem('search_history_recent_list', JSON.stringify(recent));
    console.log($.localStorage.getItem('search_history_recent_list'));
  };
}

$(window).bind( 'hashchange', _updateSearchFromHashChange);
$(window).trigger( 'hashchange' );
