function updateFromIri(iri) {
  fuseki( "metadata", iri );
  fuseki( "owner", iri);
  fuseki( "people", iri);
}

function fuseki(template_key, iri) {
  var q = $( "body" ).data(template_key).query.replace(/--IRI--/g, iri);
  $.ajax({
    url: "http://seweb.abdn.ac.uk/fuseki/ds/query",//TODO Add "timeout" and "error" to handle offline testing
    data: {
      "query" : q},
    dataType: 'json',
    success: $( "body" ).data(template_key).callback
  });  
}

function register(templateName, lines, callback) {
  $( "body" ).data(templateName, {"query": _PREAMBLE.concat(lines).join("\n"), "callback": callback});
}

$( document ).ready( function() {
  register_all_sparql_queries();
  updateFromIri( "http://dot.rural/sepake/Project#e963d657-b41f-44eb-a85d-7639346b378d" );
});

_PREAMBLE = [
             "BASE <http://dot.rural/sepake/>",
             "PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
             "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
             "PREFIX prov: <http://www.w3.org/ns/prov#>",
             "PREFIX foaf: <http://xmlns.com/foaf/0.1/>",
             ];

function register_all_sparql_queries() {
register(
      "metadata", 
      [
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
  register(
      "people",
      [
       "SELECT ?label WHERE {",
       "    BIND (<--IRI--> AS ?focus) .",
       "    {?person prov:memberOf ?focus} .",
       "    {?person rdf:type prov:Person} .",
       "    {?person rdf:type foaf:Person} .",
       "    {?person foaf:givenName ?given} .",
       "    {?person foaf:familyName ?family} .",
       "    BIND (CONCAT(?given, ' ', ?family) AS ?label)",
       "}",
       "LIMIT 1",
      ],
      function (data) {
        $( "#listOfPeople .person" ).text(data.results.bindings[0].label.value);
      });
}
