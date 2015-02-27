/**
*
*		js file for the metrics.html page
*		retrieving metrics data for either a paper or an author
*
**/

var iri = "<" + jQuery.bbq.getState('iri') + ">";

var AUTHOR_MODE = true; // true if Author related metrics are to be displayed. false otherwise.
if (iri.indexOf("PurePerson") == -1)
   AUTHOR_MODE = false;


/**
*
*		GENERIC (AUTHOR/PAPER)
*
**/
/*
	total hits for the iri
*/
// Request
// get the name separately otherwise if the paper has no hits name will be undefined
sparql("metrics_iriName",
        ["PREFIX met: <http://dot.rural/sepake/metrics/>", 
		 "SELECT ?name WHERE{",
		"{BIND ( " + iri + " AS ?x)}.",
		"{?x rdfs:label ?name }.",
		"}"
        ],
        "",
        _updateMetricPanelFromJson_iriName
    );
sparql("metrics_iriHits",
        ["PREFIX met: <http://dot.rural/sepake/metrics/>", 
		 "SELECT ?name (COUNT(*) AS ?count) WHERE{",
		"{BIND ( " + iri + " AS ?x)}.",
		"{?x met:focushit ?y }.",
		"{?x rdfs:label ?name }.",
		"} GROUP BY ?x"
        ],
        "",
        _updateMetricPanelFromJson_iriHits
    );
// Callback
function _updateMetricPanelFromJson_iriName(response) {
  var sparqlBinding = response.results.bindings[0];
  var parsed = _valuesOfSparqlBinding( sparqlBinding );
  $('#metricsPanelTitle').prepend("<p><h2>" + parsed.name + "</h2></p>");
};
// Callback
function _updateMetricPanelFromJson_iriHits(response) {
  var sparqlBinding = response.results.bindings[0];
  var parsed = _valuesOfSparqlBinding( sparqlBinding );
  $( "#metricsPanelTitle" ).after( "<p>" + (AUTHOR_MODE?" profile ":"") + "viewed " + (typeof parsed.count != 'undefined'?parsed.count:"0") + " times." + "</p>");
};

/*
	monthly breakdown of total hits for author/paper
*/
// Request
sparql("metrics_monthHits",
        ["PREFIX met: <http://dot.rural/sepake/metrics/>", 
		 "SELECT ?pref (COUNT(*) AS ?count) WHERE{",
		"BIND ( " + iri + " AS ?x).",
		"{?x met:focushit ?y  BIND ( SUBSTR(str(?y), 1, 7) AS ?pref)}.",
		"{?x rdfs:label ?name }.",
		"} GROUP BY ?pref ORDER BY DESC(?pref)"
        ],
        "",
        _updateMetricPanelFromJson_monthHits
    );
// Callback
function _updateMetricPanelFromJson_monthHits(response) {
  var arrayLength = response.results.bindings.length;
  if(arrayLength == 0
	|| jQuery.isEmptyObject(response.results.bindings[0])){
	return;
  }
  // build header
  $( "#metricsPanel tr:last" ).after( "<tr class=''></tr>" );
  $( "#metricsPanel tr:last" ).append( "<td><h3>" + "Per month" + (AUTHOR_MODE?" profile":"") + " views" + "</h3></td>" );
  // build content
  for (var i = 0; i < arrayLength; i++) {
    var sparqlBinding = response.results.bindings[i];
    var parsed = _valuesOfSparqlBinding( sparqlBinding );
	$( "#metricsPanel tr:last" ).after( "<tr class=''></tr>" );
    $( "#metricsPanel tr:last" ).append( "<td>" + parsed.pref + "</td>" );
    $( "#metricsPanel tr:last" ).append( "<td>" + parsed.count + "</td>" );
  }
};

/**
*
*		AUTHOR SPECIFICS
*
**/
/* 
	total hits for each paper of an author
*/
if(AUTHOR_MODE)
// Request
sparql("metrics_paperHits_author",
        ["PREFIX met: <http://dot.rural/sepake/metrics/>", 
		 "SELECT ?title ?name ?paperiri (COUNT(*) AS ?count) WHERE{",
		"{BIND ( " + iri +" AS ?x)}.",
		"{?x rdfs:label ?name }.",
		"{?paperiri <http://dot.rural/sepake/hasAuthor> ?x }.",
		"{?paperiri rdfs:label ?title }.",
		"{?paperiri met:focushit ?y }",
		"} GROUP BY ?paperiri"
        ],
        "",
        _updateMetricPanelFromJson_paperHits_author
    );
// Callback
function _updateMetricPanelFromJson_paperHits_author(response) {
  var arrayLength = response.results.bindings.length;
  if(arrayLength == 0
	|| jQuery.isEmptyObject(response.results.bindings[0])){
    $( "#metricsPanel tr:last" ).after( "<tr class=''></tr>" );
    $( "#metricsPanel tr:last" ).append( "<td><h3>" + "0 view of this author's publications" + "</h3></td>" );
	return;
  }
  // build header
  $( "#metricsPanel tr:last" ).after( "<tr class=''></tr>" );
  $( "#metricsPanel tr:last" ).append( "<td><h3>" + "Per publication views" + "</h3></td>" );
  // build content
  for (var i = 0; i < arrayLength; i++) {
    var sparqlBinding = response.results.bindings[i];
    var parsed = _valuesOfSparqlBinding( sparqlBinding );
	$( "#metricsPanel tr:last" ).after( "<tr class=''></tr>" );
    $( "#metricsPanel tr:last" ).append( "<td>" + parsed.title + "</td>" );
    $( "#metricsPanel tr:last" ).append( "<td>" + parsed.count + "</td>" );
  }
};