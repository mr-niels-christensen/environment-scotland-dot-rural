google.load('visualization', '1.1', {packages:['wordtree']});
google.setOnLoadCallback( function() {
    $( document ).ready( function() {
        sparql(
                [
                 "SELECT ?rdftype (COUNT(?x) AS ?xs) WHERE {",
                 "  {",
                 "    {?x rdf:type ?rdftype} .",
                 "  }",
                 "}",
                 "GROUP BY ?rdftype",
                 "ORDER BY DESC(?xs)"
                ],
                "",
                _updateDatamodelChartFromJson
        );
    });
});

function _updateDatamodelChartFromJson(response) {
    $.each(response.results.bindings, function(index, binding){
      values = _valuesOfSparqlBinding(binding);
      var brief = values.rdftype.split('/').pop();
      $( "#chartPanel" ).append( "<h2>" + brief + ": " + values.xs + " instances</h2><p id='" + brief +"'></p>");
      
    });
};

function _example(rdftype, id) {
  sparql([
          "SELECT DISTINCT ?rdftype WHERE {",
          "  {",
          "    {?x rdf:type ?rdftype} .",
          "  }",
          "}",
          "ORDER BY ?rdftype"
          ],
          values.rdftype,
          function(response) {
            //TODO
  });
}
