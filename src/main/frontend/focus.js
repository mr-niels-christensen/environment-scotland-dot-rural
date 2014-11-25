$( document ).ready( function() {
    $( document ).on( 'updateFromIri', _updateFocusFromIri);
    $( "#labelOfOwner" ).on( 'click', function() {
        var iri = $( "#labelOfOwner" ).data( 'iri');
        if (iri) {
            $( document ).trigger( 'updateFromIri', iri );  
        };
    });
});

function _updateFocusFromIri(event, iri) {
    $( '.optionalField' ).hide();
    sparql("focus",
            [
             "SELECT ?p ?y WHERE {",
             "    BIND (<--IRI--> AS ?focus) .",
             "    { ?focus ?p ?y } .",
             "}",
            ],
           iri,
           _updateFocusFromJson
    );    
}

var _predicate_to_action = {
  "http://dot.rural/sepake/ownedBy" :
    _updateOwnerFromIri,
  "http://www.w3.org/2000/01/rdf-schema#label" : 
    function( y ){ $( ".labelOfFocus" ).text(y) },
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

function _updateFocusFromJson(response) {
    try {
        var values = sparqlListToObject(response, "p", "y");
        $.each(_predicate_to_action, function( p, action ){
          action(values[p]);
        });
        if (!values["http://dot.rural/sepake/htmlDescription"]) {
          _set_html_from_dbpedia_description( "#descriptionOfFocus", values["http://www.w3.org/2000/01/rdf-schema#label"] );
        }
    } catch (err) {
      console.log( err );
    }
}

function _updateOwnerFromIri(iri) {
  if (!iri) {
    return;
  };
  $( "#labelOfOwner" ).data( 'iri', iri);
  sparql("owner",
          [
           "SELECT ?y WHERE {",
           "    BIND (<--IRI--> AS ?owner) .",
           "    { ?owner rdfs:label ?y } .",
           "}",
          ],
         iri,
         _updateOwnerFromJson
  );    
}

function _updateOwnerFromJson(response) {
  $.each(response.results.bindings, function(index, binding){
    values = _valuesOfSparqlBinding(binding);
    $( "#labelOfOwner .dataGoesHere" ).text( values.y );
    $( "#labelOfOwner" ).show();
  });
};

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

