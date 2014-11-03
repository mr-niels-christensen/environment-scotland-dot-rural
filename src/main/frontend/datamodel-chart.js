google.load('visualization', '1.1', {packages:['wordtree']});
google.setOnLoadCallback( function() {
    $( document ).ready( function() {
        sparql(
                [
                 "SELECT ?rdftype (COUNT(?x) AS ?xs) (SAMPLE(?x) AS ?sample) WHERE {",
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
      $( "#chartPanel tr:last" ).after( "<tr></tr>" );
      $( "#chartPanel tr:last" ).append( "<td>" + values.xs + "</td>" );
      $( "#chartPanel tr:last" ).append( "<td>" + values.rdftype + "</td>" );
      $( "#chartPanel tr:last" ).append( "<td>" + values.sample + "</td>" );
      $( "#chartPanel tr:last" ).append( "</tr>" );
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
