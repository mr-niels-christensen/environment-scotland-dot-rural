/*sparql("metrics",
        ["PREFIX met: <http://dot.rural/sepake/metrics/>", 
		 "SELECT (COUNT(*) AS ?count) WHERE {",
		"{BIND ( <http://dot.rural/sepake/PureProject#86ae16d9-54bb-46c6-93b1-34c9738951b6> AS ?x)}.",
		"{?x met:focushit ?y}",
		"} GROUP BY ?x"
        ],
        "",
        _updateMetricPanelFromJson
    );
*/	
sparql("metricsTitle",
		 "SELECT (?label AS ?title)  WHERE {",
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
/*
function _updateMetricPanelFromJson(response) {
  var sparqlBinding = response.results.bindings[0];
  var parsed = _valuesOfSparqlBinding( sparqlBinding );
  $('#metricsPanel').append('SUCCESS' + parsed.count);
};*/