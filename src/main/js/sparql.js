function updateFromIri(iri) {
  var q = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> ";
  q += "SELECT * WHERE {{ BIND (<" + iri + "> AS ?focus) . ";
  q += "{?focus ?relation ?object} . FILTER ( isLiteral( ?object ) ) }";
  q += "UNION {{?subject ?relation ?focus} . ";
  q += "OPTIONAL {?subject rdfs:label ?subjectLabel}}}";
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

$( document ).ready(function() {
  updateFromIri( "http://dot.rural/sepake/Project#e963d657-b41f-44eb-a85d-7639346b378d" );
})