
function _updateHistoryFromHashChange(event) {
  var recent = JSON.parse($.localStorage.getItem('search_history_recent_list')) || [];
  if (event.getState( 'query' )) {
    var new_term = event.getState( 'query' );
	var already_exist = false;
	$.each(recent, function(index, value){
	  if(value == new_term){
		already_exist = true;
		return false; // break the loop
	  }
    });
	if(!already_exist){
	  var new_len = recent.length;
	  new_len = recent.unshift(new_term);
      if (new_len > 10) {
        recent.pop();
      }
      $.localStorage.setItem('search_history_recent_list', JSON.stringify(recent));
	}
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
