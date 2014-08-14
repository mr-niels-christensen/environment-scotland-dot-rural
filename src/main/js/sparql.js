function updateFromIri(iri) {
  fuseki( "metadata", iri );
  fuseki( "owner", iri);
}

function fuseki(template_key, iri) {
  var q = $( "body" ).data(template_key).query.replace(/--IRI--/g, iri);
  $.ajax({
    url: "http://localhost:3030/ds/query",
    data: {
      "query" : q},
    dataType: 'json',
    success: $( "body" ).data(template_key).callback
  });  
}

function register(templateName, lines, callback) {
  $( "body" ).data(templateName, {"query": lines.join("\n"), "callback": callback});
}

$( document ).ready( function() {
  register(
      "metadata", 
      [
       "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
       "SELECT ?label WHERE {",
       "    BIND (<--IRI--> AS ?focus) .",
       "    {?focus rdfs:label ?label}",
       "}",
       "LIMIT 1",
      ],
      function (data) {
        $( "#labelOfFocus" ).text(data.results.bindings[0].label.value);
      });
  register(
      "owner", 
      [
       "BASE <http://dot.rural/sepake/>",
       "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
       "SELECT ?label WHERE {",
       "    BIND (<--IRI--> AS ?focus) .",
       "    {?owner <owns> ?focus} .",
       "    {?owner rdfs:label ?label}",
       "}",
       "LIMIT 1",
      ],
      function (data) {
        $( "#labelOfOwner" ).text(data.results.bindings[0].label.value);
      });
  updateFromIri( "http://dot.rural/sepake/Project#e963d657-b41f-44eb-a85d-7639346b378d" );
})
