$( document ).ready( function() {
    $( document ).on( 'updateFromIri', _updateFocusFromIri);
});

function _updateFocusFromIri(event, iri) {
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
  "http://www.w3.org/2000/01/rdf-schema#label" : 
    function( y ){ $( ".labelOfFocus" ).text(y) },
  "http://dot.rural/sepake/htmlDescription" : 
    function( y ){ $( "#descriptionOfFocus" ).html(y || "(No summary)") },
  "http://xmlns.com/foaf/0.1/homepage" : 
    function( y ){ $( "#homepageOfFocus" ).text(y || "");
                   $( "#homepageOfFocus" ).attr("href", y || "") },
  "http://www.w3.org/ns/prov#startedAtTime" : 
    function( y ){ $( "#startedAtTime" ).text(y || "(unknown)") },
  "http://www.w3.org/ns/prov#endedAtTime" : 
    function( y ){ $( "#endedAtTime" ).text(y || "(unknown)") },
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

