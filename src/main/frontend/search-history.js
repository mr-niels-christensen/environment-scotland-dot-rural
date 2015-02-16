
function _updateHistoryFromHashChange(event) {
  var recent = JSON.parse($.localStorage.getItem('search_history_recent_list')) || [];
  if (event.getState( 'query' )) {
    var new_len = recent.unshift(event.getState( 'query' ));
    if (new_len > 10) {
      recent.pop();
    };
    $.localStorage.setItem('search_history_recent_list', JSON.stringify(recent));
  };
  $( document ).ready( function() {
    $ ( "#historyTable .dynamicrow" ).remove();
    $.each(recent, function(index, term){
      $( "#historyTable tr:last" ).after( "<tr class='searchTermRow dynamicrow'></tr>" );
      $( "#historyTable tr:last" ).append( "<td>" + term + "</td>" );
    });
    $( "#historyTable .searchTermRow" ).on( 'click', function() {
      var term = $( this ).find( 'td' ).text();
      var link_url = jQuery.param.fragment( '/search.html', {'query' : term} );
      document.location.href = link_url;
  });

  });
}

$(window).bind( 'hashchange', _updateHistoryFromHashChange);
