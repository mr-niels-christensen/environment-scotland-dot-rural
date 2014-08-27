function updateFromIri(iri) {
  fuseki( "metadata", iri );
  fuseki( "owner", iri);
  fuseki( "people", iri);
}

var _FUSEKI_URLS = ["http://seweb.abdn.ac.uk/fuseki/ds/query", "http://localhost:3030/ds/query"];
var fuseki = function(template_key, iri) { console.log("Error - not initialized"); };

function initFuseki() {
  if ("file:" === $(location).attr('protocol')) { //Local testing
    _FUSEKI_URLS.reverse(); //Prefer localhost to server
  }
  fuseki = function(template_key, iri) {
    fusekiCall(
        _FUSEKI_URLS[0],
        template_key, 
        iri,
        function () { 
          fusekiCall( 
              _FUSEKI_URLS[1], 
              template_key, 
              iri, 
              function () { console.log( "No response to " + template_key + " query for " + iri ); }
          ); 
        });
  };
}

function fusekiCall(fusekiUrl, template_key, iri, errorCallback) {
  var q = $( "body" ).data(template_key).query.replace(/--IRI--/g, iri);
  $.ajax({
    url: fusekiUrl,
    data: {
      "query" : q},
    dataType: 'json',
    success: $( "body" ).data(template_key).callback,
    timeout: 2500,
    error: errorCallback,
  });
}

function register(templateName, lines, callback) {
  $( "body" ).data(templateName, {"query": _PREAMBLE.concat(lines).join("\n"), "callback": callback});
}

$( document ).ready( function() {
  initFuseki();
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
       "SELECT ?label ?comment ?homepage ?startedAtTime ?endedAtTime WHERE {",
       "    BIND (<--IRI--> AS ?focus) .",
       "    {?focus rdfs:label ?label} .",
       "    {?focus rdfs:comment ?comment} .",
       "    {?focus foaf:homepage ?homepage} .",
       "    {?focus prov:startedAtTime ?startedAtTime} .",
       "    {?focus prov:endedAtTime ?endedAtTime} .",
       "}",
       "LIMIT 1",
      ],
      function (response) {
        $( "#labelOfFocus" ).text(response.results.bindings[0].label.value);
        $( "#commentOfFocus" ).text(response.results.bindings[0].comment.value);
        $( "#homepageOfFocus" ).text(response.results.bindings[0].homepage.value);
        $( "#homepageOfFocus" ).attr("href", response.results.bindings[0].homepage.value);
        $( "#startedAtTime" ).text(response.results.bindings[0].startedAtTime.value);
        $( "#endedAtTime" ).text(response.results.bindings[0].endedAtTime.value);
      });
  register(
      "owner",
      [
       "SELECT ?label ?homepage WHERE {",
       "    BIND (<--IRI--> AS ?focus) .",
       "    {?owner <owns> ?focus} .",
       "    {?owner rdfs:label ?label} .",
       "    {?owner foaf:homepage ?homepage}",
       "}",
       "LIMIT 1",
      ],
      function (response) {
        $( "#labelOfOwner" ).text(response.results.bindings[0].label.value);
        $( "#labelOfOwner" ).attr('href', response.results.bindings[0].homepage.value);
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
