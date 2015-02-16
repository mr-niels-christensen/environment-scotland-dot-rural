$(window).bind( 'hashchange', _updateFocusFromIri);

function _updateFocusFromIri(event) {
    var iri = event.getState( 'iri' );
    $( '.optionalField' ).hide();
    sparql_predefined(
        "/sparql-queries/focus.sparql.txt", 
        {'focus' : iri}, 
        _docReady_updateFocusFromJson);    
}

var _predicate_to_action = {
  "http://www.w3.org/2000/01/rdf-schema#label" : 
    function( y ){ $( ".labelOfFocus" ).html(y) },
  "http://dot.rural/sepake/htmlDescription" : 
    function( y ){ $( "#descriptionOfFocus" ).html(y || "(No summary)") },
  "http://xmlns.com/foaf/0.1/homepage" : 
    function( y ){ 
      if (y) {
          $( "#homepageOfFocus .dataGoesHere" ).text(y);
          $( "#homepageOfFocus .dataGoesHere" ).attr("href", y);
          $( "#homepageOfFocus" ).show();
      }
  },
  "http://www.w3.org/ns/prov#startedAtTime" : 
    function( y ){ 
      if (y) {
          $( "#startedAtTime .dataGoesHere" ).text(y);
          $( "#startedAtTime" ).show();          
      };
  },
  "http://www.w3.org/ns/prov#endedAtTime" : 
    function( y ){ 
      if (y) {
          $( "#endedAtTime .dataGoesHere" ).text(y) 
          $( "#endedAtTime" ).show()          
      };
  },
};

function _docReady_updateFocusFromJson(response) {
  $( document ).ready( function() {
    _updateFocusFromJson(response)
  });
}

function _focus_is_org() {
  var iri = jQuery.bbq.getState('iri');
  if (iri) {
    var iriType = iri.match(/\/([^/]+)#/)[1];
    return (iriType == 'UKEOFOrganisation');
  } else {
    return false;
  };
}

function _updateFocusFromJson(response) {
    try {
        var values = sparqlListToObject(response, "p", "y");
        $.each(_predicate_to_action, function( p, action ){
          action(values[p]);
        });
        if (!values["http://dot.rural/sepake/htmlDescription"] && _focus_is_org()) {
          _set_html_from_dbpedia_description( "#descriptionOfFocus", values["http://www.w3.org/2000/01/rdf-schema#label"] );
        }
    } catch (err) {
      console.log( err );
    }
}

function _set_html_from_dbpedia_description(selector, search_for) {
  $.ajax({
    url: "http://lookup.dbpedia.org/api/search/KeywordSearch",
    data: {
      "QueryString" : search_for,
      "MaxHits" : 1,},
    dataType: 'json',
    success: function( response ) {
      if ( response.results[0] ) {
        $( selector ).html(response.results[0].description + " <i>[Source: Wikipedia]</i>");
      };
    },
    timeout: 2500,
  });
}

