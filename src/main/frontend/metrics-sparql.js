sparql("metrics",
        ["PREFIX met: <http://dot.rural/sepake/metrics/>", 
		 "SELECT (COUNT(*) AS ?count) WHERE {",
		"{BIND ( <http://dot.rural/sepake/PurePublication#d5408bac-08d0-4195-9d6b-659e9394ada2> AS ?x)}.",
		"{?x met:focushit ?y .}",
		"} GROUP BY ?x"
        ],
        "",
        _updateMetricPanelFromJson
    );

function _updateMetricPanelFromJson(response) {
  var sparqlBinding = response.results.bindings[0];
  var parsed = _valuesOfSparqlBinding( sparqlBinding );
  $('#metricsPanel').append('SUCCESS' + parsed.count);
};
