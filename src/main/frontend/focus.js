$( document ).ready( function() {
    $( document ).on( 'updateFromIri', _updateFocusFromIri);
});

function _updateFocusFromIri(event, iri) {
    sparql(
            [
             "SELECT * WHERE {",
             "    BIND (<--IRI--> AS ?focus) .",
             "    {?focus rdfs:label ?label} .",
             "    OPTIONAL {?focus <htmlDescription> ?description} .",
             "    OPTIONAL {?focus foaf:homepage ?homepage} .",
             "    OPTIONAL {?focus prov:startedAtTime ?startedAtTime} .",
             "    OPTIONAL {?focus prov:endedAtTime ?endedAtTime} .",
             "    OPTIONAL {?owner <owns> ?focus .",
             "              ?owner rdfs:label ?ownerLabel .",
             "              OPTIONAL {?owner foaf:homepage ?ownerHomepage}} .",
             "}",
             "LIMIT 1",
            ],
           iri,
           _updateFocusFromJson
    );    
}

function _updateFocusFromJson(response) {
    try{
        var values = _valuesOfSparqlBinding(response.results.bindings[0]);
        $( ".labelOfFocus" ).text(values.label);
        $( "#descriptionOfFocus" ).html(values.description || "(No summary)");
        $( "#homepageOfFocus" ).text(values.homepage || "");
        $( "#homepageOfFocus" ).attr("href", values.homepage || "");
        $( "#startedAtTime" ).text(values.startedAtTime || "(unknown)");
        $( "#endedAtTime" ).text(values.endedAtTime || "(unknown)");
        $( "#labelOfOwner" ).text(values.ownerLabel || "");
        $( "#labelOfOwner" ).attr('href', values.ownerHomepage || "");
        if (!values.description) {
          _set_html_from_dbpedia_description( "#descriptionOfFocus", values.label );
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

