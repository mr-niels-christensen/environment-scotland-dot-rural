var facetLabel = {'publicationYear': 'Year of publication'};

var _NEXT_PAGE_HTML = '<button type="button" class="moreLink btn btn-default btn-lg"><span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span> Next page</button>';
_NEXT_PAGE_HTML = "<tr class='dynamicrow'><td><p align='right'>" + _NEXT_PAGE_HTML + "</p></td></tr>";

function _updateSearchFromJson(response, isRefined) {
  window.scrollTo(0, 0);
  $ ( "#searchResults .dynamicrow" ).remove();
  $ ( "#searchResultsNavigation .dynamicrow" ).remove();
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
    $( "#searchResults tr:last" ).append( "<td style='text-align: right'><img height='100px' width='200px' src='" + (result.logo || "/images/missing-logo.png") + "'></td>" );
  });
  $( "#searchResults .searchResultRow" ).on( 'click', function() {
    var iri = $( this ).find( '.sepakeUri' ).text();
    var link_url = jQuery.param.fragment( '/focus.html', {'iri' : iri} );
    document.location.href = link_url;
  });
  if (response.next_cursor_websafe) {
    $( "#searchResultsNavigation").append( _NEXT_PAGE_HTML );
    var more_url = jQuery.param.fragment( '/search.html', {'query' : response.query, 'cursor_websafe' : response.next_cursor_websafe} );
    $( "#searchResultsNavigation .moreLink" ).on( 'click', function() {
      document.location.href = more_url;
    });
  }
  
  // refine search content
  if(!isRefined){
	var displayRefineSearchPanel = false;
    $ ( "#refineSearchTable .dynamicrow" ).remove();
    $.each(response.facets, function(facetKey, facetValues){
	  if(facetValues.length > 0){
	    displayRefineSearchPanel = true;
        $( "#refineSearchTable tr:last" ).after( "<tr class='facetNameRow dynamicrow'></tr>" );
        $( "#refineSearchTable tr:last" ).append( "<td><h3>" + facetLabel[facetKey] + "</h3></td>" );
	    $.each(facetValues, function(index, facetValue){
          $( "#refineSearchTable tr:last" ).after( "<tr class='facetValueRow dynamicrow'></tr>" );
          $( "#refineSearchTable tr:last" ).append( "<td>" + facetValue.label + "</td>" );
          $( "#refineSearchTable tr:last" ).append( "<td>" + facetValue.count + "</td>" );
          $( "#refineSearchTable tr:last" ).append( "<td class='refinementToken hiddenColumn'>" + facetValue.refinement_token + "</td>" );
        });
	  }
	});
	// hide / show the refine search panel 
	if(displayRefineSearchPanel){
	  $ ( "#refineSearchPanel" ).show();
	}
	else{ // none of the facet returned has got data
	  $ ( "#refineSearchPanel" ).hide();
	}
    $( "#refineSearchTable .facetValueRow" ).on( 'click', function() {
      //var refinement_tokens = [];
	  //refinement_tokens.push($( this ).find( 'td.refinementToken' ).text());
	  var refinement_token = $( this ).find( 'td.refinementToken' ).text();
	  search_terms = jQuery.bbq.getState( 'query' ) || 'environment';
	  search(search_terms, refinement_token, null, _docReady_updateSearchFromJsonWithRefinement);
    });
  }
}

function _docReady_updateSearchFromJsonWithRefinement(response) {
  $( document ).ready( function (){
    _updateSearchFromJson(response, true);
  });
}

function _docReady_updateSearchFromJson(response) {
  $( document ).ready( function (){
    _updateSearchFromJson(response, false);
  });
}

function _updateSearchFromHashChange(event) {
  var query = event.getState( 'query' ) || 'environment';
  var cursor_websafe =  event.getState( 'cursor_websafe' ) || null;
  search(query, null, cursor_websafe, _docReady_updateSearchFromJson);
}

$(window).bind( 'hashchange', _updateSearchFromHashChange);

