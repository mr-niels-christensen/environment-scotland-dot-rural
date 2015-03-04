/**
*
*		js file for the metrics.html page
*		retrieving metrics data for either a paper or an author
*
**/
var START_DATE = "2014-11"; // the official launch of the service; date from which to display the per month hits breakdown

var iri = jQuery.bbq.getState('iri');
var iri_wrapped = "<" + jQuery.bbq.getState('iri') + ">";

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
		"{BIND ( " + iri_wrapped + " AS ?x)}.",
		"{?x rdfs:label ?name }.",
		"}"
        ],
        "",
        _updateMetricPanelFromJson_iriName
    );
sparql("metrics_iriHits",
        ["PREFIX met: <http://dot.rural/sepake/metrics/>", 
		 "SELECT ?name (COUNT(*) AS ?count) WHERE{",
		"{BIND ( " + iri_wrapped + " AS ?x)}.",
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
  $('#metricsPanelTitle').prepend("<p><h2 class='metricsLink'>" + parsed.name + "</h2></p>");
  $( "#metricsPanelTitle .metricsLink" ).on( 'click', function() {
	var link_url = jQuery.param.fragment( '/focus.html', {'iri' : iri}  );
	document.location.href = link_url;
  });
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
		 "SELECT ?date_month ?date_year ?sorting_date ?y (COUNT(*) AS ?count) WHERE{",
		"BIND ( " + iri_wrapped + " AS ?x).",
		"{?x met:focushit ?y  BIND ( SUBSTR(str(?y), 1, 7) AS ?sorting_date) BIND ( SUBSTR(?sorting_date, 6, 7) AS ?date_month ) BIND ( SUBSTR(?sorting_date, 1, 4) AS ?date_year )}.",
		"{?x rdfs:label ?name }.",
		"} GROUP BY ?sorting_date ORDER BY DESC(?sorting_date)"
        ],
        "",
        _updateMetricPanelFromJson_monthHits
    );
	// BIND ( (CONCAT(SUBSTR(?sorting_date, 6, 7),'-',SUBSTR(?sorting_date, 1, 4))) AS ?display_date)
	// BIND ( (CONCAT(STR(MONTH(?y)),'-',STR(YEAR(?y)))) AS ?display_date)
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
  var now_date = getNowDate();
  var current_date = now_date;
  for (var i = 0; i < arrayLength; i++) {
    var sparqlBinding = response.results.bindings[i];
    var parsed = _valuesOfSparqlBinding( sparqlBinding );
	// fill in the empty rows up to the current item
	current_date = generateEmptyRows(current_date, parsed.sorting_date, false);
	
	generateRowForDate(parsed.date_year, parsed.date_month, parsed.count);
	current_date = decrementDate(current_date);
	
	if(i == arrayLength - 1){
	  // fill in the empty remaining rows up to the starting date
	  generateEmptyRows(current_date, START_DATE, true);
	}
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
		"{BIND ( " + iri_wrapped +" AS ?x)}.",
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
	$( "#metricsPanel tr:last" ).after( "<tr></tr>" );
    $( "#metricsPanel tr:last" ).append( "<td class='metricsLink'>" + parsed.title + "<span class='paperiri' style='visibility: hidden'>" + parsed.paperiri + "</span>" + "</td>" );
    $( "#metricsPanel tr:last" ).append( "<td>" + parsed.count + "</td>" );
	$( "#metricsPanel .metricsLink" ).on( 'click', function() {
	  var iri = $( this ).find( 'span' ).text();
	  var link_url = jQuery.param.fragment( '/focus.html', {'iri' : iri}  );
	  document.location.href = link_url;
    });
  }
};

/**
*		UTILS
**/

						/*********************************/
						/*	for Per month breakdown	 */
						/*********************************/

/**
*  generate html empty rows for the months with no hits from current_date to to_date (dates are strings formatted yyyy-mm)
*  returns the decremented current_date accordingly
**/
function generateEmptyRows(current_date, to_date, include_to_date){
  while( isAfter(current_date, to_date) || (include_to_date?current_date == START_DATE:false)){
		var from_year = current_date.substring(0, 4);
		var from_month = current_date.substring(5, 7);
		generateRowForDate(from_year, from_month, 0);
		current_date = decrementDate(current_date);
  }
  return current_date;
}

/**
*  generate html for an row for the given year, month and hit count
**/
function generateRowForDate(year, month, count){
	$( "#metricsPanel tr:last" ).after( "<tr class=''></tr>" );
    $( "#metricsPanel tr:last" ).append( "<td>" + month + "-" + year + "</td>" );
    //$( "#metricsPanel tr:last" ).append( "<td>" + parsed.sorting_date + "</td>" );
    $( "#metricsPanel tr:last" ).append( "<td>" + count + "</td>" );
}

/**
*  return true if date is after ref_date  (dates are strings formatted yyyy-mm)
**/	
function isAfter(date, ref_date){
	var date_year = parseInt(date.substring(0, 4));
	var date_month = parseInt(date.substring(5, 7));
	var ref_date_year = parseInt(ref_date.substring(0, 4));
	var ref_date_month = parseInt(ref_date.substring(5, 7));
	
	if(date_year >  ref_date_year){
		return true;
	}
	if(date_year ==  ref_date_year){
		return date_month > ref_date_month;
	}
	return false;
}

/**
*  return the date date decremented by a month  (dates formatted as yyyy-mm)
**/
function decrementDate(date){
  var year = date.substring(0, 4);
  var month = date.substring(5, 7);
	if(month > 1){
		month--;
	}
	else{
		month = 12;
		year--;
	}
	if(month.toString().length == 1){
	  month = "0" + month ;
	}
	return year + "-" + month;
}

/**
*	return "yyyy-mm" format for the current date
**/
function getNowDate(){
  var today = new Date();
  var month = today.getMonth() + 1; // month numbered from 0
  var year = today.getFullYear();
  if(month.toString().length == 1){
	  month = "0" + month ;
  }
  var res = year.toString() + "-" + month.toString();
  return res;
}