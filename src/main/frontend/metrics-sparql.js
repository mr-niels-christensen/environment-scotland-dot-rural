/*
sparql("metrics",
        ["PREFIX met: <http://dot.rural/sepake/metrics/>", 
		 "SELECT (COUNT(*) AS ?count) WHERE {",
		"{BIND ( <http://dot.rural/sepake/PureProject#86ae16d9-54bb-46c6-93b1-34c9738951b6> AS ?x)}.",
		"{?x met:focushit ?y}",
		"} GROUP BY ?x"
        ],
        "",
        _updateMetricPanelFromJson
    );

	
sparql("metricsTitle",
		["SELECT (?label AS ?title)  WHERE {",
		"{BIND ( <http://dot.rural/sepake/PureProject#86ae16d9-54bb-46c6-93b1-34c9738951b6> AS ?x)}.",
		"{?x rdfs:label ?label}",
		"}"
        ],
        "",
        _updateMetricPanelTitleFromJson
    );
	
function _updateMetricPanelTitleFromJson(response) {
  var sparqlBinding = response.results.bindings[0];
  var parsed = _valuesOfSparqlBinding( sparqlBinding );
  $('#metricsPanel').append(parsed.title);
};
function _updateMetricPanelFromJson(response) {
  var sparqlBinding = response.results.bindings[0];
  var parsed = _valuesOfSparqlBinding( sparqlBinding );
  $('#metricsPanel').append('SUCCESS' + parsed.count);
};

*/

/**
*
*		AUTHOR HITS PAGE
*
**/
/* total hits for the author */
/*PREFIX met: <http://dot.rural/sepake/metrics/>
SELECT ?name (COUNT(*) AS ?count) WHERE{
	{BIND ( <http://dot.rural/sepake/PurePerson#3a0b45bc-fd6d-4c59-adac-e52a2711e785> AS ?x)}.
	{?x met:focushit ?y }.
	{?x rdfs:label ?name }.
} GROUP BY ?x*/
sparql("metrics_authorHits",
        ["PREFIX met: <http://dot.rural/sepake/metrics/>", 
		 "SELECT ?name (COUNT(*) AS ?count) WHERE{",
		"{BIND ( <http://dot.rural/sepake/PurePerson#3a0b45bc-fd6d-4c59-adac-e52a2711e785> AS ?x)}.",
		"{?x met:focushit ?y }.",
		"{?x rdfs:label ?name }.",
		"} GROUP BY ?x"
        ],
        "",
        _updateMetricPanelFromJson_authorHits
    );

/* total hits for each paper of an author */
sparql("metrics_paperHits_author",
        ["PREFIX met: <http://dot.rural/sepake/metrics/>", 
		 "SELECT ?title ?name ?paperiri (COUNT(*) AS ?count) WHERE{",
		"{BIND ( <http://dot.rural/sepake/PurePerson#3a0b45bc-fd6d-4c59-adac-e52a2711e785> AS ?x)}.",
		"{?x rdfs:label ?name }.",
		"{?paperiri <http://dot.rural/sepake/hasAuthor> ?x }.",
		"{?paperiri rdfs:label ?title }.",
		"{?paperiri met:focushit ?y }",
		"} GROUP BY ?paperiri"
        ],
        "",
        _updateMetricPanelFromJson_paperHits_author
    );
	
function _updateMetricPanelFromJson_paperHits_author(response) {
  var sparqlBinding = response.results.bindings[0];
  var parsed = _valuesOfSparqlBinding( sparqlBinding );
  $('#metricsPanel').append('count:' + parsed.count);
  $('#metricsPanel').append('; name:' + parsed.name);
  $('#metricsPanel').append('; title:' + parsed.title);
};
function _updateMetricPanelFromJson_authorHits(response) {
  var sparqlBinding = response.results.bindings[0];
  var parsed = _valuesOfSparqlBinding( sparqlBinding );
  $('#metricsPanel').append('count:' + parsed.count);
  $('#metricsPanel').append('; name:' + parsed.name);
};