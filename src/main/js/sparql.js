var BODY_DATA_KEY_SPARQL_TEMPLATE = "SPARQL_TEMPLATE";

function updateFromIri(iri) {
  var q = $( "body" ).data(BODY_DATA_KEY_SPARQL_TEMPLATE).replace(/--IRI--/g, iri);
  $.ajax({
    url: "http://localhost:3030/ds/query",
    data: {
      "query" : q},
    dataType: 'json',
    success: updateFromData
  });
}

function updateFromData( data ) {
  console.log(data);
}

$( document ).ready( function() {
  $( "body" ).data(BODY_DATA_KEY_SPARQL_TEMPLATE, 
      [
       "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
       "SELECT * WHERE {{ BIND (<--IRI--> AS ?focus) .",
       "{?focus ?relation ?object} . FILTER ( isLiteral( ?object ) ) }",
       "UNION {{?subject ?relation ?focus} .",
       "OPTIONAL {?subject rdfs:label ?subjectLabel}}}"
      ].join("\n"));
  updateFromIri( "http://dot.rural/sepake/Project#e963d657-b41f-44eb-a85d-7639346b378d" );
})
