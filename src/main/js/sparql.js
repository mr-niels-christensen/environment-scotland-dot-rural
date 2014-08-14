function updateFromIri(iri) {
  var q = $( "body" ).data("metadata").replace(/--IRI--/g, iri);
  $.ajax({
    url: "http://localhost:3030/ds/query",
    data: {
      "query" : q},
    dataType: 'json',
    success: updateFromData
  });
}

function updateFromData( data ) {
  bindings = data.results.bindings;
  console.log(bindings);
  for (index in bindings) {
    if (bindings[index].relation.value === "http://www.w3.org/2000/01/rdf-schema#label") {
      $( "#labelOfFocus" ).text(bindings[index].value.value)
    }
  }
}

$( document ).ready( function() {
  $( "body" ).data("test", 
      [
       "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
       "SELECT * WHERE {",
       "    BIND (<--IRI--> AS ?focus) .",
       "    {?subject ?relation ?focus} .",
       "    {?subject ?labelType ?subjectLabel} .",
       "    FILTER ( isLiteral ( ?subjectLabel ) )",
       "}",
      ].join("\n"));
  $( "body" ).data("metadata", 
      [
       "SELECT * WHERE {",
       "    BIND (<--IRI--> AS ?focus) .",
       "    {?focus ?relation ?value} .",
       "    FILTER ( isLiteral ( ?value ) )",
       "}",
      ].join("\n"));
  updateFromIri( "http://dot.rural/sepake/Project#e963d657-b41f-44eb-a85d-7639346b378d" );
})
