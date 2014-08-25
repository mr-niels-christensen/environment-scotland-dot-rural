function updateFromIri(iri) {
  fuseki( "metadata", iri );
  fuseki( "owner", iri);
  fuseki( "people", iri);
}

function fuseki(template_key, iri) {
  var q = $( "body" ).data(template_key).query.replace(/--IRI--/g, iri);
  $.ajax({//TODO Add "timeout" and "error" to handle network failiures and offline testing
    url: "http://seweb.abdn.ac.uk/fuseki/ds/query",//Local testing with "http://localhost:3030/ds/query"
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
       "SELECT ?label ?comment WHERE {",
       "    BIND (<--IRI--> AS ?focus) .",
       "    {?focus rdfs:label ?label} .",
       "    {?focus rdfs:comment ?comment}",
       "}",
       "LIMIT 1",
      ],
      function (response) {
        $( "#labelOfFocus" ).text(response.results.bindings[0].label.value);
        $( "#commentOfFocus" ).text(response.results.bindings[0].comment.value);
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
      function (response) {
        $( "#labelOfOwner" ).text(response.results.bindings[0].label.value);
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
       "ORDER BY ASC(?family)",
       "LIMIT 11",
      ],
      function (response) {
        var bindings = response.results.bindings;
        $( "#personList .personWrapper" ).each( function(index, dom_elem) {//TODO: #personList -> .personList to allow several
          if (bindings.length > 0) {
            $( dom_elem ).data( bindings.shift() );
            $( dom_elem ).find( ".personLink" ).text( $( dom_elem ).data().label.value );
            $( dom_elem ).addClass( "hasData" );      
            $( dom_elem ).removeClass( "noData" );
          } else {
            $( dom_elem ).removeClass( "hasData" );      
            $( dom_elem ).addClass( "noData" );                  
          }
        });
        if (bindings.length > 0) { //More results to display
          $( "#personList" ).addClass( "hasMore" );
          $( "#personList" ).removeClass( "noMore" );
        } else {
          $( "#personList" ).removeClass( "hasMore" );
          $( "#personList" ).addClass( "noMore" );          
        }
      });
}
