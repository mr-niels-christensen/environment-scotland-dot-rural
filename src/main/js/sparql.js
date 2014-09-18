function updateFromIri(iri) {
  fuseki( "metadata", iri );
  fuseki( "people", iri);
}

var _FUSEKI_URLS = {
    "http:" : "http://seweb.abdn.ac.uk/fuseki/ds/query", 
    "file:" : "http://localhost:3030/ds/query"};

var fuseki = function(template_key, iri) { console.log("Error - not initialized"); };

function initFuseki() {
  fuseki = function(template_key, iri) {
    fusekiCall(
        _FUSEKI_URLS[$(location).attr('protocol')],
        template_key, 
        iri,
        function () { 
          console.log( "No response to " + template_key + " query for " + iri );
          $( "#myAjaxAlert" ).removeClass( "hide" );
        });
  };
}

function fusekiCall(fusekiUrl, template_key, iri, errorCallback) {
  var q = $( "body" ).data( "sparql-" + template_key).query.replace(/--IRI--/g, iri);
  $.ajax({
    url: fusekiUrl,
    data: {
      "query" : q},
    dataType: 'json',
    success: $( "body" ).data( "sparql-" + template_key).callback,
    timeout: 2500,
    error: errorCallback,
  });
}

function register(templateName, lines, callback) {
  $( "body" ).data( "sparql-" + templateName, {"query": _PREAMBLE.concat(lines).join("\n"), "callback": callback});
}

$( document ).ready( function() {
  initFuseki();
  register_all_sparql_queries();
  indexJsInit();
  updateFromIri( "https://catalogue.ukeof.org.uk/id/412d0ac7-5b16-4ba9-b72f-4b6da92310eb" );
});

function _valuesOfSparqlBinding( sparqlBinding ) {
  var result = {};
  for (key in sparqlBinding) {
    result[key] = sparqlBinding[key].value;
  }
  return result;
}

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
       "SELECT * WHERE {",
       "    BIND (<--IRI--> AS ?focus) .",
       "    {?focus rdfs:label ?label} .",
       "    OPTIONAL {?focus rdfs:comment ?comment} .",
       "    OPTIONAL {?focus foaf:homepage ?homepage} .",
       "    OPTIONAL {?focus prov:startedAtTime ?startedAtTime} .",
       "    OPTIONAL {?focus prov:endedAtTime ?endedAtTime} .",
       "    OPTIONAL {?owner <owns> ?focus .",
       "               ?owner rdfs:label ?ownerLabel .",
       "               ?owner foaf:homepage ?ownerHomepage} .",
       "}",
       "LIMIT 1",
      ],
      function (response) {
        try{
          var values = _valuesOfSparqlBinding(response.results.bindings[0]);
          $( "#labelOfFocus" ).text(values.label);
          $( "#commentOfFocus" ).html(values.comment.split("\n").join("</p><p>") || "(No summary)");
          $( "#homepageOfFocus" ).text(values.homepage || "");
          $( "#homepageOfFocus" ).attr("href", values.homepage || "");
          $( "#startedAtTime" ).text(values.startedAtTime || "(unknown)");
          $( "#endedAtTime" ).text(values.endedAtTime || "(unknown)");
          $( "#labelOfOwner" ).text(values.ownerLabel || "");
          $( "#labelOfOwner" ).attr('href', values.ownerHomepage || "");
        } catch (err) {
          console.log( err );
        }
      });
  register(
      "people",
      [
       "SELECT * WHERE {",
       "    BIND (<--IRI--> AS ?focus) .",
       "    {?person prov:memberOf ?focus} .",
       "    {?person rdf:type prov:Person} .",
       "    {?person rdf:type foaf:Person} .",
       "    {?person foaf:givenName ?given} .",
       "    {?person foaf:familyName ?family} .",
       "    {?person foaf:mbox ?mbox} .",
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
            $( dom_elem ).find( ".personLink" ).attr('title', $( dom_elem ).data().mbox.value );
            $( dom_elem ).removeClass( "noData" );
          } else {
            $( dom_elem ).addClass( "noData" );                  
          }
        });
        if (bindings.length > 0) { //More results to display
          $( "#personList" ).removeClass( "noMore" );
        } else {
          $( "#personList" ).addClass( "noMore" );          
        }
      });
  register(
      "searchables", 
      [
       "SELECT * WHERE {",//TODO: Get type, but only one record per id, maybe using #3
       "    {?id rdfs:label ?label} .",
       "    {?id rdfs:comment ?comment} .",
       "}",
      ],
      function (response) {
        $( "#search" ).trigger( "preloaded", {items: $.map( response.results.bindings, function(binding, index) {
          return _valuesOfSparqlBinding(binding);
        })});
      });
}
