$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
     ajaxStop: function() { $body.removeClass("loading"); }    
});

$( "#searchForm" ).submit(function( event ) {
  event.preventDefault();
  var link_url = jQuery.param.fragment( '/search.html', {'query' : $( '#search' ).val()} );
  document.location.href = link_url; 
});

$( document ).ajaxError(function( event, jqxhr, settings, thrownError ) {
    if ($( "#myAjaxAlert" ).queue( "fx" ).length == 0) {
        //NOTE: Without parameters, show() and hide() do not queue nicely
        $( "#myAjaxAlert" ).show(400).delay(2500).hide(400);
    }
	// display the Exception message for the query form page data.html
	var exceptionText = getException(jqxhr.responseText)
	if(typeof exceptionText == 'undefined')
		exceptionText = "Error with no exception raised";
	$( "#sparqlResponse" ).append( "<p id='ExceptionMessage'>" + exceptionText + "</p>" );
});

function search(query, cursor_websafe, callback) {
  $.ajax({
    url: "/search/default",
    data: {
      "query" : query,
      "cursor_websafe" : cursor_websafe},
    dataType: 'json',
    success: callback,
    timeout: 19000 + 2000 * Math.random() //20 seconds +-1 
  });
}

function sparql_predefined(queryUrl, parameters, callback) {
  var data = { "queryUrl" : queryUrl };
  for (key in parameters) {
    data[key] = parameters[key];    
  }
  $.ajax({
    url: "/sparql/default/predefined.json",
    data: data,
    dataType: 'json',
    success: callback,
    timeout: 19000 + 2000 * Math.random() //20 seconds +-1 
  });
}

function sparql(name, queryAsList, iri, callback) {
    var q = _PREAMBLE.concat(queryAsList).join("\n").replace(/--IRI--/g, iri);
    $.ajax({
      url: "/sparql/default/dynamic.json",
      data: {
          "name" : name,
        "query" : q},
      dataType: 'json',
      success: callback,
      timeout: 19000 + 2000 * Math.random() //20 seconds +-1 
    });
}

function sparql_nondefault_graph(graph_id, name, queryAsList, iri, callback) {
  var q = _PREAMBLE.concat(queryAsList).join("\n").replace(/--IRI--/g, iri);
  $.ajax({
    url: "/sparql/" + graph_id + "/dynamic.json",
    data: {
        "name" : name,
      "query" : q},
    dataType: 'json',
    success: callback,
    timeout: 19000 + 2000 * Math.random() //20 seconds +-1 
  });
}

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
    var arrayForThisKey = result[values[keyName]] || [];
    result[values[keyName]] = arrayForThisKey;
    arrayForThisKey.push(values[valueName]);
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

 /**
 * UTILS
 **/
// returns the substring starting with "Exception:" and finishing with "</pre>"
function getException(str){
  var start = "Exception:";
  var end = "</pre>";
  var startindex = str.indexOf(start);
  var endindex = str.indexOf(end, startindex);
  if (startindex !=-1 && endindex !=-1 &&  endindex  > startindex )
	return decodeHtml(str.substring(startindex , endindex ));	
}

function decodeHtml(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}