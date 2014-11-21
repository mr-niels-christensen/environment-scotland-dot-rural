$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
     ajaxStop: function() { $body.removeClass("loading"); }    
});

$( document ).ajaxError(function( event, request, settings ) {
    if ($( "#myAjaxAlert" ).queue( "fx" ).length == 0) {
        //NOTE: Without parameters, show() and hide() do not queue nicely
        $( "#myAjaxAlert" ).show(400).delay(2500).hide(400);        
    } 
});

function sparql(name, queryAsList, iri, callback) {
    var q = _PREAMBLE.concat(queryAsList).join("\n").replace(/--IRI--/g, iri);
    $.ajax({
      url: _FUSEKI_URLS[$(location).attr('protocol')],
      data: {
          "name" : name,
        "query" : q},
      dataType: 'json',
      success: callback,
      timeout: 20000
    });
}

var _FUSEKI_URLS = {
    "http:" : "/sparql/current/query.json", 
    "file:" : "http://localhost:3030/ds/query"
};

function _valuesOfSparqlBinding( sparqlBinding ) {
  var result = {};
  for (key in sparqlBinding) {
    result[key] = sparqlBinding[key].value;
  }
  return result;
}

function sparqlListToObject( sparqlResponse, keyName, valueName ) {
  var result = {};
  $.each(sparqlResponse.results.bindings, function( index, binding ){
    values = _valuesOfSparqlBinding(binding);
    result[values[keyName]] = values[valueName];
  });
  return result;
}

_PREAMBLE = [
             "BASE <http://dot.rural/sepake/>",
             "PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
             "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
             "PREFIX prov: <http://www.w3.org/ns/prov#>",
             "PREFIX foaf: <http://xmlns.com/foaf/0.1/>",
             ];

